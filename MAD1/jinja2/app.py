import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from jinja2 import Template


DATA_FILE = "data.csv"
OUTPUT_FILE = "output.html"
PLOT_FILE = "bar-chart.png"


def load_data():
    return pd.read_csv(DATA_FILE)


def save_html(html):
    with open(OUTPUT_FILE, "w") as f:
        f.write(html)
    print("HTML generated successfully.")


def error_page():
    template = Template("""
    <html>
    <head><title>Error</title></head>
    <body>
        <h2>Invalid Input</h2>
        <p>Please check the arguments.</p>
    </body>
    </html>
    """)
    save_html(template.render())
    sys.exit()


# STUDENT MODE
def student_mode(df, student_id):
    student_df = df[df["Student id"] == student_id]

    if student_df.empty:
        error_page()

    total_marks = student_df["Marks"].sum()

    template = Template("""
    <html>
    <head>
        <title>Student Report</title>
        <style>
            table { border-collapse: collapse; }
            th, td { border: 1px solid black; padding: 0px; }
        </style>
    </head>
    <body>
        <h2>Student Report</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Course</th>
                <th>Marks</th>
            </tr>
            {% for r in rows %}
            <tr>
                <td>{{ r['Student id'] }}</td>
                <td>{{ r['Course id'] }}</td>
                <td>{{ r['Marks'] }}</td>
            </tr>
            {% endfor %}
            <tr>
                <td colspan="2"><b>Total</b></td>
                <td><b>{{ total }}</b></td>
            </tr>
        </table>
    </body>
    </html>
    """)

    html = template.render(rows=student_df.to_dict("records"),
                           total=total_marks)
    save_html(html)


# COURSE MODE
def course_mode(df, course_id):
    course_df = df[df["Course id"] == course_id]

    if course_df.empty:
        error_page()

    avg_marks = course_df["Marks"].mean()
    highest = course_df["Marks"].max()

    generate_chart(course_df["Marks"])

    template = Template("""
    <html>
    <head>
        <title>Course Report</title>
    </head>
    <body>
        <h2>Course Summary</h2>
        <table border="1">
            <tr>
                <th>Average</th>
                <th>Highest</th>
            </tr>
            <tr>
                <td>{{ avg }}</td>
                <td>{{ max }}</td>
            </tr>
        </table>
        <br>
        <img src="bar-chart.png" width="500">
    </body>
    </html>
    """)

    html = template.render(avg=round(avg_marks, 2),
                           max=highest)
    save_html(html)


def generate_chart(series):
    counts = series.value_counts().sort_index()

    plt.figure()
    plt.bar(counts.index, counts.values)
    plt.xlabel("Marks")
    plt.ylabel("Count")
    plt.title("Marks Distribution")
    plt.savefig(PLOT_FILE)
    plt.close()


# MAIN
def main():
    if len(sys.argv) < 3:
        error_page()

    df = load_data()
    option = sys.argv[1]

    try:
        value = int(sys.argv[2])
    except ValueError:
        error_page()

    if option == "-s":
        student_mode(df, value)
    elif option == "-c":
        course_mode(df, value)
    else:
        error_page()


if __name__ == "__main__":
    main()
