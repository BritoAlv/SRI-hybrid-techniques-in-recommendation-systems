using BookshelfApp.Entities;

namespace BookshelfApp.Contracts.Responses;

public record FeaturesResponse(
    List<string> Genres,
    List<string> Authors,
    List<TimePeriods> TimePeriods
);