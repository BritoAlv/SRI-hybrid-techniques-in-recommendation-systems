using BookshelfApp.Entities;
using Microsoft.EntityFrameworkCore;

namespace BookshelfApp.DataAccess;

public class BookshelfContext : DbContext
{
    public DbSet<User> Users { get; set; } = null!;
    public DbSet<Book> Books { get; set; } = null!;
    public DbSet<Genre> Genres { get; set; } = null!;
    public DbSet<UserBook> UserBooks { get; set; } = null!;

    public BookshelfContext(DbContextOptions<BookshelfContext> options) : base(options) { }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // A user-book is uniquely determined by its user-id and its book-id
        modelBuilder.Entity<UserBook>()
            .HasIndex(userBook => new
            {
                userBook.UserId,
                userBook.BookId
            })
            .IsUnique();

        // A user is uniquely determined by its email address
        modelBuilder.Entity<User>()
            .HasIndex(user => new
            {
                user.Email
            })
            .IsUnique();
    }
}