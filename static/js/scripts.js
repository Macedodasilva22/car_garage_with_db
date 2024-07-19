document.addEventListener('DOMContentLoaded', () => {
    // Handle add car form submission
    document.getElementById('addCarForm')?.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        fetch('/add_car', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => alert(data))
        .catch(error => console.error('Error:', error));
    });

    // Handle search cars form submission
    document.getElementById('searchCarsForm')?.addEventListener('submit', (event) => {
        event.preventDefault();
        const name = document.getElementById('name').value;
        fetch(`/search_cars?name=${encodeURIComponent(name)}`)
            .then(response => response.json())
            .then(data => {
                const resultsDiv = document.getElementById('searchResults');
                resultsDiv.innerHTML = '<table><tr><th>ID</th><th>Name</th><th>Image</th></tr>';
                data.forEach(car => {
                    resultsDiv.innerHTML += `<tr><td>${car.id}</td><td>${car.name}</td><td><img src="${car.img}" alt="${car.name}" width="100"></td></tr>`;
                });
                resultsDiv.innerHTML += '</table>';
            })
            .catch(error => console.error('Error:', error));
    });

    // Handle add problem form submission
    document.getElementById('addProblemForm')?.addEventListener('submit', (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        fetch('/add_problem', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => alert(data))
        .catch(error => console.error('Error:', error));
    });

    // Handle car problems form submission
    document.getElementById('carProblemsForm')?.addEventListener('submit', (event) => {
        event.preventDefault();
        const carId = document.getElementById('car_id').value;
        fetch(`/car_problems/${carId}`)
            .then(response => response.json())
            .then(data => {
                const resultsDiv = document.getElementById('carProblemsResults');
                resultsDiv.innerHTML = '<table><tr><th>ID</th><th>Car Name</th><th>Problem</th><th>Cost</th><th>Status</th></tr>';
                data.forEach(problem => {
                    resultsDiv.innerHTML += `<tr><td>${problem.id}</td><td>${problem.name}</td><td>${problem.description}</td><td>${problem.cost}</td><td>${problem.status}</td></tr>`;
                });
                resultsDiv.innerHTML += '</table>';
            })
            .catch(error => console.error('Error:', error));
    });
});
