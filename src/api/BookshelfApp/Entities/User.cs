namespace BookshelfApp;

public class User
{
    // Main Properties
    public Guid Id { get; set; }
    public string Name { get; set; } = null!;
    public string Email { get; set; } = null!;

    // Relational Properties
    public ICollection<UserBook> UserBooks { get; set; } = null!;
}