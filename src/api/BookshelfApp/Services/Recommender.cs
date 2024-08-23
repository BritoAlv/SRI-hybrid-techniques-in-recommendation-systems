using BookshelfApp.DataAccess;
using Microsoft.Extensions.Options;
using Python.Runtime;

namespace BookshelfApp.Services;

public class Recommender
{
    private dynamic _recommender;
    
    public Recommender(IOptions<RecommenderSettings> settings)
    {
        Runtime.PythonDLL = settings.Value.PythonDLL;
        PythonEngine.Initialize();
        dynamic sys = Py.Import("sys");
        sys.path.append("../../scripts");
        var pythonScript = Py.Import("recommender");
        _recommender = pythonScript.InvokeMethod("start");
    }

    public List<int> Recommend(int userId)
    {   
        var recommendation = new List<int>();
        var results = _recommender.recommend(new PyInt(userId));

        foreach (var pair in results)
        {
            var bookId = (int)int.Parse(pair[1].ToString());
            recommendation.Add(bookId);
        }

        return recommendation;
    }
}