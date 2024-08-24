using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;

namespace BookshelfApp.DataAccess;

public class BookshelfContextFactory : IDesignTimeDbContextFactory<BookshelfContext>
{
    public BookshelfContext CreateDbContext(string[] args)
    {
        var optionsBuilder = new DbContextOptionsBuilder<BookshelfContext>();
        optionsBuilder.UseSqlite(args[0]);

        return new BookshelfContext(optionsBuilder.Options);
    }
}