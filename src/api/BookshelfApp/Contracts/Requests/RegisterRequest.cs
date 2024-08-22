namespace BookshelfApp.Contracts.Requests;

public record RegisterRequest(
    string Name,
    string Email
);