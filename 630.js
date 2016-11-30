window.onload = function() { 
adjacency("nodelist_cs1.csv","edgelist_cs1.csv");

}
function barchart(infile){
var margin = {top: 20, right: 40, bottom: 70, left: 40},
    width = 400 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

// Parse the date / time

var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

var y = d3.scale.linear().range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10);

var svg = d3.select("#area2")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", 
          "translate(" + margin.left + "," + margin.top + ")");

d3.csv(infile, function(error, data) {

    data.forEach(function(d) {
        d.date = d.date;
        d.value = +d.value;
    });
	
  x.domain(data.map(function(d) { return d.date; }));
  y.domain([0, d3.max(data, function(d) { return d.value; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", "-.55em")
      .attr("transform", "rotate(-90)" );

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")

  svg.selectAll("bar")
      .data(data)
    .enter().append("rect")
      .style("fill", "steelblue")
      .attr("x", function(d) { return x(d.date); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.value); })
      .attr("height", function(d) { return height - y(d.value); });

});
}
function parallel(input){
var margin = {top: 30, right: 10, bottom: 10, left: 10},
    width = 400 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;



var line = d3.svg.line(),
    axis = d3.svg.axis().orient("left"),
    background,
    foreground;
function path(d) {
    return line(dimensions.map(function(p) { return [x(p), y[p](d[p])]; }));
}

// Handles a brush event, toggling the display of foreground lines.
function brush() {
    var actives = dimensions.filter(function(p) { return !y[p].brush.empty(); }),
    extents = actives.map(function(p) { return y[p].brush.extent(); });
    foreground.style("display", function(d) {
        return actives.every(function(p, i) {
            return extents[i][0] <= d[p] && d[p] <= extents[i][1];
        }) ? null : "none";
    });
}

var x = d3.scale.ordinal().rangePoints([0, width], 1),
    y = {};
var svg_parallel = d3.select("#area1")
.attr("width", width + margin.left + margin.right)
.attr("height", height + margin.top + margin.bottom)
.append("g")
.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.csv(input, function(error, cars) {

    // Extract the list of dimensions and create a scale for each.
    x.domain(dimensions = d3.keys(cars[0]).filter(function(d) {
        return d != "name" && (y[d] = d3.scale.linear()
                //.domain(d3.extent(cars, function(p) { return +p[d]; }))
		.domain([0,100])
                .range([height, 0]));
    }
));
    // Add grey background lines for context.
    background = svg_parallel.append("g")
        .attr("class", "background")
        .selectAll("path")
        .data(cars)
        .enter().append("path")
        .attr("d", path);

    // Add blue foreground lines for focus.
    foreground = svg_parallel.append("g")
        .attr("class", "foreground")
        .selectAll("path")
        .data(cars)
        .enter().append("path")
        .attr("d", path);

    // Add a group element for each dimension.
    var g = svg_parallel.selectAll(".dimension")
        .data(dimensions)
        .enter().append("g")
        .attr("class", "dimension")
        .attr("transform", function(d) { return "translate(" + x(d) + ")"; });

    // Add an axis and title.
    g.append("g")
        .attr("class", "axis")
        .each(function(d) { d3.select(this).call(axis.scale(y[d])); })
        .append("text")
        .style("text-anchor", "middle")
        .attr("y", -9)
        .text(function(d) { return d; });

    // Add and store a brush for each axis.
    g.append("g")
        .attr("class", "brush")
        .each(function(d) { d3.select(this).call(y[d].brush = d3.svg.brush().y(y[d]).on("brush", brush)); })
        .selectAll("rect")
        .attr("x", -8)
        .attr("width", 16);
});
}




function adjacency(node,edge) {

    queue()
    .defer(d3.csv, node)
    .defer(d3.csv, edge)
    .await(function(error, file1, file2) { createAdjacencyMatrix(file1, file2); });
    
    function createAdjacencyMatrix(nodes,edges) {
      var edgeHash = {};
      for (x in edges) {
        var id = edges[x].source + "-" + edges[x].target;
        edgeHash[id] = edges[x];
      }
      matrix = [];
      //create all possible edges
      for (a in nodes) {
        for (b in nodes) {
          var grid = {id: nodes[a].id + "-" + nodes[b].id, x: b, y: a, weight: 0};
          if (edgeHash[grid.id]) {
            grid.weight = edgeHash[grid.id].weight;
          }
          matrix.push(grid);
        }
      }

var matrix_height,matrix_width;
matrix_height = 800;
matrix_width = 800;
      var matrix2 = d3.select("#vizcontainer")
      .attr("width", matrix_width + 100)
      .attr("height",matrix_height + 100)
      .append("g")
      .attr("transform", "translate(50,50)")
      .attr("id", "adjacencyG")
      .call(d3.behavior.zoom().on("zoom", function () {
        matrix2.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
	text_header1.attr("transform", "translate(" + (d3.event.translate) + ")" + " scale(" + d3.event.scale + ")");
	text_header2.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
    }))
      .selectAll("rect")
      .data(matrix)
      .enter()
      .append("rect")
      .attr("width", matrix_width/ nodes.length)
      .attr("height", matrix_height/ nodes.length)
      .attr("x", function (d) {return d.x * (matrix_width/ nodes.length)})
      .attr("y", function (d) {return d.y * (matrix_height/ nodes.length)})
      .style("stroke", "black")
      .style("stroke-width", "1px")
      .style("fill", "red")
      .style("fill-opacity", function (d) {return d.weight * .2})
      .on("mouseover", gridOver)
      .on("click",function (d,i){
d3.select("#area1").select("g").remove();
d3.select("#area2").select("g").remove();
parallel("./parallel_coordinate_data/" + nodes[d.y].id + '-' + nodes[d.x].id+ ".txt");
barchart("./bar_chart_data/" + nodes[d.y].id + ".csv");
//barchart("bar-data.csv");
	})

      var scaleSize = nodes.length * (matrix_width/ nodes.length);
      var nameScale = d3.scale.ordinal().domain(nodes.map(function (el) {return el.id})).rangePoints([0,scaleSize],1);

      xAxis = d3.svg.axis().scale(nameScale).orient("top").tickSize(4);    
      yAxis = d3.svg.axis().scale(nameScale).orient("left").tickSize(4);
	var text_header1 = d3.select("#adjacencyG").append("g").call(xAxis);
        var text_content1 = text_header1.selectAll("text").style("text-anchor", "end");//;
	text_content1.attr("transform", "translate(-10,-10) rotate(90)");
     	var text_header2 = d3.select("#adjacencyG").append("g").call(yAxis);

      function gridOver(d,i) {
        d3.selectAll("rect").style("stroke-width", function (p) {return p.x == d.x || p.y == d.y ? "3px" : "1px"})
      }

    }

    
  }
