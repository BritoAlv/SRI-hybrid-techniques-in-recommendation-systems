namespace BookshelfApp;

class Book
{
    // Main Properties
    public Guid Id { get; set; }
    public string Name { get; set; } = null!;
    public string Author { get; set; } = null!;
    public string Language { get; set; } = null!;
    public int Year { get; set; }

    // Relational Properties
    public ICollection<Genre> Genres { get; set; } = null!;
    public ICollection<UserBook> UserBooks { get; set; } = null!;
}