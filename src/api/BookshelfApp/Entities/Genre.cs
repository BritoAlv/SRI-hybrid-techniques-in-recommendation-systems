using System.ComponentModel.DataAnnotations;

namespace BookshelfApp.Entities;

public class Genre
{
    // Main Properties
    [Key]
    public string Name { get; set; } = null!;

    // Relational Properties
    public ICollection<Book> Books {get; set;} = null!;
}