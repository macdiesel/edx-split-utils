$(function() {
    // Hide the info pane initially eles.one()
    $("#info-pane").hide();
    // Create and set up the graph.
    $('#cy').cytoscape({
        style: cytoscape.stylesheet()
            .selector('node')
                .css({
                    'content': 'data(name)',
                    'text-valign': 'center'
                })
            .selector('edge')
                .css({
                    'target-arrow-shape': 'triangle'
                }),

        elements: {
            nodes: [
                {data: { id: "n1", name: "node 1" }},
                {data: { id: "n2", name: "node 2" }}
            ],
            edges: [
                {data: { id: "e1", source: "n1", target: "n2" }}
            ]
        },

        layout: {
            name: 'dagre',
            rankDir: 'TB'
        },
        ready: function() {
            window.cy = this;
            cy.elements().unselectify();
            cy.on('tap', function(e){
                var node = e.cyTarget;
                $("#info-pane").text(node.data('name'));
                $("#info-pane").show();

            });
        }
    });
});
