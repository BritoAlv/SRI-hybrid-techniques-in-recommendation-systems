using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace BookshelfApp.Migrations
{
    /// <inheritdoc />
    public partial class AddfeaturescolumninUsers : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "Features",
                table: "Users",
                type: "TEXT",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Features",
                table: "Users");
        }
    }
}
