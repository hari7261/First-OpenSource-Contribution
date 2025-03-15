let students = [];

function renderStudents() {
  const studentListContainer = document.getElementById("studentList");
  studentListContainer.innerHTML = "";

  students.forEach(student => {
    const studentDiv = document.createElement("div");
    studentDiv.classList.add("student-item");

    const studentInfo = `
      Roll No: ${student.rollNo}, 
      Name: ${student.name}, 
      Department: ${student.department}, 
      Class: ${student.class}, 
      Seminar Topic: ${student.seminarTopic}
    `;

    const studentSpan = document.createElement("span");
    studentSpan.textContent = studentInfo;
    studentDiv.appendChild(studentSpan);
    studentListContainer.appendChild(studentDiv);
  });
}

function saveStudent() {
  const rollNo = document.getElementById("rollNo").value.trim();
  const name = document.getElementById("name").value.trim();
  const department = document.getElementById("department").value.trim();
  const className = document.getElementById("class").value.trim();
  const seminarTopic = document.getElementById("seminarTopic").value.trim();

  if (rollNo && name && department && className && seminarTopic) {
    // Save the student details
    students.push({
      rollNo,
      name,
      department,
      class: className,
      seminarTopic
    });

    // Clear the input fields
    document.getElementById("rollNo").value = "";
    document.getElementById("name").value = "";
    document.getElementById("department").value = "";
    document.getElementById("class").value = "";
    document.getElementById("seminarTopic").value = "";

    // Show success popup
    alert("Your details have been enrolled successfully!");

    // Re-render student list
    renderStudents();
  } else {
    alert("Please fill in all fields!");
  }
}

// Initial render
renderStudents();
