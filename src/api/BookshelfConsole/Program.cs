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

// foreach(var book in db.Books)
//     Console.WriteLine($"{book.Name} written by {book.Author}");

// db.SaveChanges();

using Python.Runtime;

Runtime.PythonDLL = "/snap/gnome-42-2204/172/usr/lib/python3.10/config-3.10-x86_64-linux-gnu/libpython3.10.so";
PythonEngine.Initialize();

using(Py.GIL())
{
    dynamic sys = Py.Import("sys");
    // Sensitive Data:
    sys.path.append ("/home/javier/Core/Computer Science/Projects/IRS/SRI-hybrid-techniques-in-recommendation-systems/src/scripts");
    var pythonScript = Py.Import("recommender");

    dynamic pyUtilityMatrix = pythonScript.InvokeMethod("utility_matrix");
    dynamic pyLshMatrix = pythonScript.InvokeMethod("lsh_matrix", pyUtilityMatrix);
    

    while(true)
    {
        Console.WriteLine("Enter user id: ");
        var input = Console.ReadLine();
        dynamic recommended = pythonScript.InvokeMethod("recommend_books", pyUtilityMatrix, pyLshMatrix, new PyInt(int.Parse(input!)));
        Console.WriteLine(recommended);
    }

}

Console.WriteLine("Tra");