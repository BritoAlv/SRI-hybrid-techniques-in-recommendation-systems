namespace BookshelfApp.Contracts;

public record UserRequest(
    string Name,
    string Email,
    List<string> Genres,
    List<string> Authors,
    List<int> TimePeriods
);