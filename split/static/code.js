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
                }),

        elements: {
            nodes: [],
            edges: []
        },

        layout: {
            name: 'grid',
            padding: 10
        },
        ready: function() {
            window.cy = this;
            cy.elements().unselectify();
            cy.on('tap', function(e){
                var node = e.cyTarget;
                $("#info-pane").text(node.data('name'));
                $("#info-pane").show();

            });
            cy.add([
                    { group: "nodes", data: { id: "n1", name: "node 1" }, position: { x: 100, y: 100 } },
                    { group: "nodes", data: { id: "n2", name: "node 2" }, position: { x: 100, y: 200 } },
                    { group: "edges", data: { id: "e1", source: "n1", target: "n2" } },

            ]);
        }
    });
});
