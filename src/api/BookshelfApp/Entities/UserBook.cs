namespace BookshelfApp;

public class UserBook
{
    // Main Properties
    public float ReadRatio { get; set; }
    public int Rating { get; set; }
    public string Comment { get; set; } = null!;
    public int Shared { get; set; }

    // Relational Properties
    public Guid BookId { get; set; }
    public Guid UserId { get; set; }
}