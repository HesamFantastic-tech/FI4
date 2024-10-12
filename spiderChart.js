window.onload = function() {
    // Fetch the data passed from Flask (use Jinja2 template to pass variables)
    const labels = {{ questions_list | tojson }};
    const values = {{ average_values | tojson }};
    
    // Define data for the radar chart
    var data = [{
        type: 'scatterpolar',
        r: values,  // The values
        theta: labels,  // The labels/questions
        fill: 'toself',
        name: 'User Responses'
    }];

    // Layout configuration
    var layout = {
        polar: {
            radialaxis: {
                visible: true,
                range: [0, 5]  // Set the range for the values (adjust as needed)
            }
        },
        showlegend: false  // Hide the legend if not needed
    };

    // Create the plot in the div with id 'spiderChart'
    Plotly.newPlot('spiderChart', data, layout);
};
