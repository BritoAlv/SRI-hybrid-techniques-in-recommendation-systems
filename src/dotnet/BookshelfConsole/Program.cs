using Python.Runtime;

Runtime.PythonDLL = "/snap/gnome-42-2204/172/usr/lib/python3.10/config-3.10-x86_64-linux-gnu/libpython3.10.so";
PythonEngine.Initialize();

using (Py.GIL())
{
    dynamic sys = Py.Import("sys");
    sys.path.append("../../scripts");

    var pythonScript = Py.Import("recommender");
    dynamic recommender = pythonScript.InvokeMethod("start");

    while (true)
    {
        Console.WriteLine("Enter user id: ");
        var input = Console.ReadLine();
        Console.WriteLine(recommender.recommend(new PyInt(input!)));
    }
}