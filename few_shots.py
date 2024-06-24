few_shots = [
    {
        'Question': "What is the crude prevalence of asthma in Bellwood?",
        'SQLQuery': "SELECT Data_Value FROM health_data WHERE LocationName = 'Bellwood' AND Measure = 'Current asthma' AND Data_Value_Type = 'Crude prevalence';",
        'SQLResult': "Result of the SQL query",
        'Answer': "11"
    },
    {
        'Question': "List all the locations where the prevalence of stroke is above 7%.",
        'SQLQuery': "SELECT LocationName FROM health_data WHERE Measure = 'Stroke ' AND Data_Value > 3;",
        'SQLResult': "Result of the SQL query",
        'Answer': "['Brooklyn','Alorton','Brooklyn','Alorton','East St. Louis','Centreville','Centreville','Hopkins Park','Robbins','Pulaski','Washington Park']"
    },
    {
        'Question': "Show me the locations with the highest prevalence of obesity.",
        'SQLQuery': "SELECT LocationName, MAX(Data_Value) AS HighestPrevalenceOfObesity FROM health_data WHERE Measure = 'Obesity' GROUP BY LocationName ORDER BY HighestPrevalenceOfObesity DESC LIMIT 10;",
        'SQLResult': "Result of the SQL query",
        'Answer': "['(Brooklyn 60.4)','(Centreville 59.5)','(Alorton 59.4)','(Washington Park 58.3)','(East St. Louis 57.9)','(Venice 54.9)','(Sauget 51.9)','(Cahokia 51.9)','(Hopkins Park 50.6)','(Madison 49.7)']"
    },
    {
        'Question': "List all the locations where the prevalence of depression is above 10%.",
        'SQLQuery': "SELECT LocationName FROM health_data WHERE Measure = 'Depression' AND Data_Value > 10;",
        'SQLResult': "Result of the SQL query",
        'Answer': "['East St. Louis','Centreville','Washington Park','Madison','Venice']"
    }
]
    