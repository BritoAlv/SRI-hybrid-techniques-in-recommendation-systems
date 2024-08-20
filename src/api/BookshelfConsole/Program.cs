// using BookshelfApp.DataAccess;
// using BookshelfApp.Entities;
// using Microsoft.EntityFrameworkCore;
// using Microsoft.Extensions.Configuration;

// var configurationBuilder = new ConfigurationBuilder();
// configurationBuilder.SetBasePath(Directory.GetCurrentDirectory())
//                     .AddJsonFile("./appsettings.json", optional: false, reloadOnChange: true);

// var configuration = configurationBuilder.Build();

// var connectionString = configuration.GetConnectionString("BookshelfConnection");

// var options = new DbContextOptionsBuilder<BookshelfContext>().UseSqlite(connectionString!).Options;

// var db = new BookshelfContext(options);

// foreach (var ub in db.UserBooks)
//     Console.WriteLine(ub.Id);

// db.Books.Add(new Book()
// {
//     Name = "Quijote",
//     Author = "Pancho",
//     Language = "En",
// });

// db.Books.Add(new Book()
// {
//     Name = "Iliada",
//     Author = "Pancho",
//     Language = "En",
// });

// db.Books.Add(new Book()
// {
//     Name = "Crimen",
//     Author = "Pancho",
//     Language = "En",
// });

// db.Books.Add(new Book()
// {
//     Name = "Paz",
//     Author = "Pancho",
//     Language = "En",
// });

// db.Books.Add(new Book()
// {
//     Name = "Galia",
//     Author = "Pancho",
//     Language = "En",
// });

// db.Books.Add(new Book()
// {
//     Name = "Sol",
//     Author = "Pancho",
//     Language = "En",
// });

// db.Books.Add(new Book()
// {
//     Name = "Mar",
//     Author = "Pancho",
//     Language = "En",
// });

// db.SaveChanges();

using Python.Runtime;

Runtime.PythonDLL = "/snap/gnome-42-2204/172/usr/lib/python3.10/config-3.10-x86_64-linux-gnu/libpython3.10.so";
PythonEngine.Initialize();

using(Py.GIL())
{
    dynamic sys = Py.Import("sys");
    sys.path.append ("/home/javier/Core/Computer Science/Projects/IRS/SRI-hybrid-techniques-in-recommendation-systems/src/api/scripts");
    var pythonScript = Py.Import("main");
    dynamic pyUtilityMatrix = pythonScript.InvokeMethod("utility_matrix");
    dynamic pyLshMatrix = pythonScript.InvokeMethod("lsh_matrix", pyUtilityMatrix);
    pythonScript.InvokeMethod("foo", pyUtilityMatrix);
}

Console.WriteLine("Tra");