using BookshelfApp.Contracts;
using BookshelfApp.DataAccess;
using BookshelfApp.Entities;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);
var connectionString = builder.Configuration.GetConnectionString("BookshelfConnection");

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddDbContext<BookshelfContext>(options =>
    options.UseSqlite(connectionString)
);

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();
app.UseHttpsRedirection();


// Register endpoint
app.MapPost("/bookshelf/register", (UserRequest request, BookshelfContext context) => {
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


// Login endpoint
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

app.Run();
