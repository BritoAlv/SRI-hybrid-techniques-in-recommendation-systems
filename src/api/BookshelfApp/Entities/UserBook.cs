using System.ComponentModel.DataAnnotations;

namespace BookshelfApp.Entities;

public class UserBook
{
    // Main Properties
    [Key]
    public int Id { get; set; }
    public float ReadRatio { get; set; }
    public int? Rating { get; set; }
    public string? Comment { get; set; } = null;
    public int Shared { get; set; }

    // Relational Properties
    public int BookId { get; set; }
    public int UserId { get; set; }
}