namespace BookshelfApp.Contracts;

public record UserBookContract(
    int UserId,
    int BookId,
    float ReadRatio,
    string Comment,
    int Shared,
    int Rating
);