function reloadGraph(nodes, edges) {
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
            })
            .selector('node[root]')
            .css({
                'background-color': 'red'
            })
            .selector('node[current]')
            .css({
                'background-color': 'green'
            }),

        elements: {nodes: nodes, edges: edges},

        layout: {
            name: 'dagre',
            rankDir: 'TB'
        },
        ready: function () {
            window.cy = this;
            cy.elements().unselectify();
            cy.on('mouseover', function (e) {
                var node = e.cyTarget;
                retrieveStructureInfo(node.data('id'));
            });
        }
    });
};
