using System.ComponentModel.DataAnnotations;

namespace BookshelfApp.Entities;

public class User
{
    // Main Properties
    [Key]
    public int Id { get; set; }
    public string Name { get; set; } = null!;
    public string Email { get; set; } = null!;
    public string? Features { get; set; } = null!;

    // Relational Properties
    public ICollection<UserBook> UserBooks { get; set; } = null!;
}