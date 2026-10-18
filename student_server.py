from fastmcp import FastMCP

mcp = FastMCP("Student Records")

students = {
    101: {"name": "Ali Ahmed", "course": "Computer Science", "grade": "A", "attendance": "92%", "fee_due": 500},
    102: {"name": "Sara Khan", "course": "Data Science", "grade": "B+", "attendance": "85%", "fee_due": 0},
    103: {"name": "John Smith", "course": "Artificial Intelligence", "grade": "A-", "attendance": "90%", "fee_due": 250},
}


@mcp.tool()
def get_student_attendance(student_id: int) -> dict:
    """Get a student's attendance percentage using their student ID."""
    student = students.get(student_id)
    if student is None:
        return {"error": "Student not found"}
    return {"name": student["name"], "attendance": student["attendance"]}

@mcp.tool()
def get_course_info(student_id: int) -> dict:
    """Get the course a student is enrolled in using their student ID."""
    student = students.get(student_id)
    if student is None:
        return {"error": "Student not found"}
    return {"name": student["name"], "course": student["course"]}


@mcp.tool()
def get_student_result(student_id: int) -> dict:
    """Get a student's full result and details using their student ID."""
    return students.get(student_id, {"error": "Student not found"})
@mcp.tool()
def get_fee_due(student_id: int) -> dict:
    """Get the amount of fee a student still owes using their student ID."""
    student = students.get(student_id)
    if student is None:
        return {"error": "Student not found"}
    return {"name": student["name"], "fee_due": student["fee_due"]}

if __name__ == "__main__":
    mcp.run()