// Horários fixos
const times = ["08:00","10:00","11:30","14:00","16:00","19:00"];

// Referências ao DOM
const daysContainer = document.getElementById("days");
const slotsContainer = document.getElementById("timeslots");

let selectedDayElem = null;

let selectedDate = null;
let selectedTime = null;

function generateCalendar() {
  const today = new Date();
  const year = today.getFullYear();
  const month = today.getMonth();

  const firstDayWeekday = new Date(year, month, 1).getDay();
  const totalDays = new Date(year, month + 1, 0).getDate();

  for (let i = 0; i < firstDayWeekday; i++) {
    daysContainer.appendChild(document.createElement("div"));
  }

  for (let day = 1; day <= totalDays; day++) {
    const div = document.createElement("div");
    div.textContent = day;
    if (day === today.getDate()) div.classList.add("today");

    div.addEventListener("click", () => {
      if (selectedDayElem) selectedDayElem.classList.remove("selected");
      div.classList.add("selected");
      selectedDayElem = div;

      // Salva a data selecionada
      selectedDate = new Date(year, month, day);
      updateHiddenField();

      generateSlots();
    });

    daysContainer.appendChild(div);
  }
}

function generateSlots() {
  slotsContainer.innerHTML = "";
  times.forEach(time => {
    const btn = document.createElement("button");
    btn.type = "button"; // evita submit
    btn.textContent = time;
    btn.addEventListener("click", () => {
      slotsContainer.querySelectorAll("button").forEach(b => b.classList.remove("selected"));
      btn.classList.add("selected");

      selectedTime = time;
      updateHiddenField();
    });
    slotsContainer.appendChild(btn);
  });
}

function updateHiddenField() {
  if (selectedDate && selectedTime) {
    const dataFormatada = selectedDate.toISOString().split("T")[0]; // yyyy-mm-dd
    const fullDateTime = `${dataFormatada} ${selectedTime}`;
    document.getElementById("data_horario").value = fullDateTime;
    console.log("Selecionado:", fullDateTime); // debug opcional
  }
}

document.addEventListener("DOMContentLoaded", () => {
  generateCalendar();
});


// // Função que gera o calendário do mês atual
// function generateCalendar() {
//   const today = new Date();
//   const year = today.getFullYear();
//   const month = today.getMonth();

//   const firstDayWeekday = new Date(year, month, 1).getDay();
//   const totalDays = new Date(year, month + 1, 0).getDate();

//   // Preenche espaços vazios antes do dia 1
//   for (let i = 0; i < firstDayWeekday; i++) {
//     daysContainer.appendChild(document.createElement("div"));
//   }

//   // Cria cada dia
//   for (let day = 1; day <= totalDays; day++) {
//     const div = document.createElement("div");
//     div.textContent = day;
//     if (day === today.getDate()) div.classList.add("today");

//     div.addEventListener("click", () => {
//       // marca o dia selecionado
//       if (selectedDayElem) selectedDayElem.classList.remove("selected");
//       div.classList.add("selected");
//       selectedDayElem = div;
//       // (re)gera horários
//       generateSlots();
//     });

//     daysContainer.appendChild(div);
//   }
// }

// // Função que gera os botões de horário
// function generateSlots() {
//   slotsContainer.innerHTML = "";
//   times.forEach(time => {
//     const btn = document.createElement("button");
//     btn.textContent = time;
//     btn.type = "button"
//     btn.addEventListener("click", () => {
//       // marca o horário selecionado
//       slotsContainer.querySelectorAll("button").forEach(b => b.classList.remove("selected"));
//       btn.classList.add("selected");
//     });
//     slotsContainer.appendChild(btn);
//   });
// }

// // Inicializa o calendário na carga de página
// document.addEventListener("DOMContentLoaded", () => {
//   generateCalendar();
// });
