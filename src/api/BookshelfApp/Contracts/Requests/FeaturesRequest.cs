namespace BookshelfApp.Contracts.Requests;

public record FeaturesRequest(
    int UserId,
    List<string> Genres,
    List<string> Authors,
    List<int> TimePeriods
);