using System.Text.Json;
using BookshelfApp.Contracts;
using BookshelfApp.Contracts.Requests;
using BookshelfApp.Contracts.Responses;
using BookshelfApp.DataAccess;
using BookshelfApp.Entities;
using BookshelfApp.Services;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.EntityFrameworkCore;
using Python.Runtime;

var builder = WebApplication.CreateBuilder(args);

// Runtime.PythonDLL = builder.Configuration.GetSection("PythonDLL").Value;
// PythonEngine.Initialize();

var bookshelfConnection = builder.Configuration.GetConnectionString("BookshelfConnection");

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddDbContext<BookshelfContext>(options =>
    options.UseSqlite(bookshelfConnection)
);

builder.Services.Configure<RecommenderSettings>(builder.Configuration.GetSection(nameof(RecommenderSettings)));
builder.Services.AddSingleton<Recommender>();

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();
app.UseHttpsRedirection();


// Register endpoint
app.MapPost("/bookshelf/register", (RegisterRequest request, BookshelfContext context) => {
    var users = context.Users;
    // Query for email
    var user = users.FirstOrDefault(user => user.Email == request.Email);

    // Verify email's not been registered
    if (user != null)
        return Results.BadRequest(new ErrorResponse("Email is already registered"));
    
    // Persist on db
    user = new User() { Name = request.Name, Email = request.Email};
    users.Add(user);
    context.SaveChanges();

    return Results.Ok(new UserResponse(user.Id, user.Email));
});

// Login endpoint
app.MapPost("/bookshelf/login", (LoginRequest request, BookshelfContext context) => {
    var users = context.Users;
    // Query for email
    var user = users.FirstOrDefault(user => user.Email == request.Email);

    // Verify email's been registered
    if (user == null)
        return Results.BadRequest(new ErrorResponse("Email is not registered"));
    
    return Results.Ok(new UserResponse(user.Id, user.Email));
});

// User features get endpoint
app.MapGet("/bookshelf/features", (BookshelfContext context) => {
    var genres = context.Genres.Select(g => g.Name).ToList();
    
    var response = new FeaturesResponse(
        genres,
        [],
        [TimePeriods.Ancient, TimePeriods.Modern, TimePeriods.Contemporary]
    );

    return Results.Ok(response);
});

// User features post endpoint
app.MapPost("/bookshelf/features", (FeaturesRequest request, BookshelfContext context) => {
    var user = context.Users.FirstOrDefault(u => u.Id == request.UserId);

    if (user == null)
        return Results.BadRequest(new ErrorResponse("UserId was not found"));
    
    dynamic features = new {
        request.Genres,
        request.Authors,
        request.TimePeriods
    };

    features = JsonSerializer.Serialize(features);
    user.Features = features;
    context.SaveChanges();

    return Results.Ok();
});

// Rating endpoint
app.MapPost("/bookshelf/rating", (UserBookContract request, BookshelfContext context) => {
    var usersBooks = context.UserBooks;
    var userBook = usersBooks.FirstOrDefault(u => u.BookId == request.BookId && request.UserId == u.UserId);

    if (userBook == null)
    {
        userBook = new UserBook()
        {
            BookId = request.BookId,
            UserId = request.UserId,
            Rating = request.Rating,
            ReadRatio = request.ReadRatio,
            Shared = request.Shared,
            Comment = request.Comment
        };
        usersBooks.Add(userBook);
        context.SaveChanges();
    }
    else
    {
        var updated = new UserBook() {
            BookId = request.BookId,
            UserId = request.UserId,
            Rating = request.Rating,
            ReadRatio = request.ReadRatio > userBook.ReadRatio ? request.ReadRatio : userBook.ReadRatio,
            Shared = request.Shared > userBook.Shared ? request.Shared : userBook.Shared,
            Comment = request.Comment
        };

        usersBooks.Attach(updated);
        context.Entry(updated).State = EntityState.Modified;
        context.SaveChanges();
    }
    
    return Results.Ok();
});

// Search endpoint
app.MapGet("/bookshelf/search", (string query, BookshelfContext context) => {
    var books = context.Books.Where(b => b.Name.Contains(query.ToLower())).Select(b => new Tuple<int, string>(b.Id, b.Name)).ToList();

    return Results.Ok(books);
});

//  Implement recommend method
app.MapGet("/bookshelf/recommend", (int userId, Recommender recommender) => {
    return Results.Ok(recommender.Recommend(userId));
});

app.Run();
