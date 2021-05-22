#include <iostream>
#include <vector>

#include "planar_dual.hpp"

using namespace boost;

template <typename Graph>
void print_graph(Graph &g)
{
  std::cout << "vertices: " << std::endl;
  typename graph_traits<Graph>::vertex_iterator vi, vi_end;
  for (tie(vi, vi_end) = vertices(g); vi != vi_end; ++vi)
  {
    std::cout << *vi << std::endl;
  }

  std::cout << "edges: " << std::endl;
  typename graph_traits<Graph>::edge_iterator ei, ei_end;
  for (tie(ei, ei_end) = edges(g); ei != ei_end; ++ei)
  {
    std::cout << *ei << "," << std::endl;
  }
}

void get_dual(dualgraph::graph &g, dualgraph::graph &dual_g)
{
  // Create the graph - two triangles that share an edge

  // Create an empty graph to hold the dual
  // dualgraph::graph dual_g;

  //Initialize the interior edge index

  property_map<dualgraph::graph, edge_index_t>::type e_index = boost::get(edge_index, g);
  graph_traits<dualgraph::graph>::edges_size_type edge_count = 0;
  graph_traits<dualgraph::graph>::edge_iterator ei, ei_end;
  for (tie(ei, ei_end) = edges(g); ei != ei_end; ++ei)
  {
    put(e_index, *ei, edge_count++);
  }

  // Compute the planar embedding - we know the input graph is planar,
  // so we're ignoring the return value of the test
  typedef std::vector<graph_traits<dualgraph::graph>::edge_descriptor> vec_t;
  std::vector<vec_t> embedding(num_vertices(g));
  boyer_myrvold_planarity_test(boyer_myrvold_params::graph = g,
                               boyer_myrvold_params::embedding = &embedding[0]);

  create_dual_graph(g, dual_g, &embedding[0]);
}

int get_graph_edge_num(dualgraph::graph &dual_g)
{
  // calculate the edge number of input dual graph.
  int n_dual_node = 0;

  typedef property_map<dualgraph::graph, vertex_index_t>::type IndexMap;
  IndexMap index = boost::get(vertex_index, dual_g);

  typename graph_traits<dualgraph::graph>::edge_iterator ei, ei_end;
  int i = 0;
  for (tie(ei, ei_end) = edges(dual_g); ei != ei_end; ++ei)
  {
    n_dual_node++;
  }
  return n_dual_node;
}

void get_dual_graph(int size, int* edge_origin, dualgraph::graph &dual_g)
{
  // Generate the dual graph from original input.
  dualgraph::graph g;
  for (int i = 0; i < size; i++)
  {
    add_edge(edge_origin[i*2+0], edge_origin[i*2+1], g);
  }

  get_dual(g, dual_g);
}

int *get_dual_edges(dualgraph::graph &dual_g)
{
  int dual_size = get_graph_edge_num(dual_g);

  // calculate dual edges memories.
  int (*edge_dual)[2] = new int[dual_size][2];

  // get edge pairs.
  typedef property_map<dualgraph::graph, vertex_index_t>::type IndexMap;
  IndexMap index = boost::get(vertex_index, dual_g);

  typename graph_traits<dualgraph::graph>::edge_iterator ei, ei_end;
  int i = 0;
  for (tie(ei, ei_end) = edges(dual_g); ei != ei_end; ++ei)
  {
    edge_dual[i][0] = index[source(*ei, dual_g)];
    edge_dual[i][1] = index[target(*ei, dual_g)];
    i++;
  }
  return *edge_dual;
}

int* get_dual_edges(dualgraph::graph &dual_g,int dual_size)
{

  // calculate dual edges memories.
  int (*edge_dual)[2] = new int[dual_size][2];

  // get edge pairs.
  typedef property_map<dualgraph::graph, vertex_index_t>::type IndexMap;
  IndexMap index = boost::get(vertex_index, dual_g);

  typename graph_traits<dualgraph::graph>::edge_iterator ei, ei_end;
  int i = 0;
  for (tie(ei, ei_end) = edges(dual_g); ei != ei_end; ++ei)
  {
    edge_dual[i][0] = index[source(*ei, dual_g)];
    edge_dual[i][1] = index[target(*ei, dual_g)];
    i++;
  }
  return *edge_dual;
}
