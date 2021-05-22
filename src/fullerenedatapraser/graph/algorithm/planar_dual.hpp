#ifndef __CREATE_DUAL_GRAPH_HPP__
#define __CREATE_DUAL_GRAPH_HPP__

#include <vector>

#include <boost/config.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/property_map/property_map.hpp>
#include <boost/graph/planar_face_traversal.hpp>
#include <boost/tuple/tuple.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/boyer_myrvold_planar_test.hpp>

namespace boost
{

  template <typename InputGraph,
            typename OutputGraph,
            typename EdgeIndexMap>
  struct dual_graph_visitor : public planar_face_traversal_visitor
  {

    typedef typename graph_traits<OutputGraph>::vertex_descriptor vertex_t;
    typedef typename graph_traits<InputGraph>::edge_descriptor edge_t;
    typedef typename std::vector<vertex_t> vertex_vector_t;
    typedef iterator_property_map<typename vertex_vector_t::iterator, EdgeIndexMap>
        edge_to_face_map_t;

    dual_graph_visitor(InputGraph &arg_g,
                       OutputGraph &arg_dual_g,
                       EdgeIndexMap arg_em) : g(arg_g),
                                              dual_g(arg_dual_g),
                                              em(arg_em),
                                              edge_to_face_vector(num_edges(g),
                                                                  graph_traits<OutputGraph>::null_vertex()),
                                              edge_to_face(edge_to_face_vector.begin(), em)
    {
    }

    void begin_face()
    {
      current_face = add_vertex(dual_g);
    }

    template <typename Edge>
    void next_edge(Edge e)
    {
      vertex_t existing_face = edge_to_face[e];
      if (existing_face == graph_traits<OutputGraph>::null_vertex())
      {
        edge_to_face[e] = current_face;
      }
      else
      {
        add_edge(existing_face, current_face, dual_g);
      }
    }

    InputGraph &g;
    OutputGraph &dual_g;
    EdgeIndexMap em;
    vertex_t current_face;
    vertex_vector_t edge_to_face_vector;
    edge_to_face_map_t edge_to_face;
  };

  template <typename InputGraph,
            typename OutputGraph,
            typename PlanarEmbedding,
            typename EdgeIndexMap>
  void create_dual_graph(InputGraph &g,
                         OutputGraph &dual_g,
                         PlanarEmbedding embedding,
                         EdgeIndexMap em)
  {
    dual_graph_visitor<InputGraph, OutputGraph, EdgeIndexMap>
        visitor(g, dual_g, em);
    planar_face_traversal(g, embedding, visitor, em);
  }

  template <typename InputGraph,
            typename OutputGraph,
            typename PlanarEmbedding>
  void create_dual_graph(InputGraph &g,
                         OutputGraph &dual_g,
                         PlanarEmbedding embedding)
  {
    create_dual_graph(g, dual_g, embedding, get(edge_index, g));
  }

} // namespace boost


namespace dualgraph
{
  using namespace boost;
  typedef adjacency_list<vecS,
                         vecS,
                         undirectedS,
                         property<vertex_index_t, int>,
                         property<edge_index_t, int>>
      graph;
}
template <typename Graph>
void print_graph(Graph &g);
void get_dual(dualgraph::graph &g, dualgraph::graph &dual_g);
int get_graph_edge_num(dualgraph::graph &dual_g);
void get_dual_graph(int size, int* edge_origin, dualgraph::graph &dual_g);
int *get_dual_edges(dualgraph::graph &dual_g);
int *get_dual_edges(dualgraph::graph &dual_g, int n_dual_node);

namespace dualgraph
{
  class dual_graph_generator
  {
  public:
    int origin_size;
    int *edge_origin;
    int dual_size;
    dual_graph_generator(int size, int* edge_origin)
    {
      origin_size = size;
      get_dual_graph(size, edge_origin, dual_g);
      privacy_get_graph_edge_num();
    }
    ~dual_graph_generator(){

    }
    void dual_graph_generator::privacy_get_graph_edge_num()
    {
      dual_size = get_graph_edge_num(dual_g);
    }
    int *dual_graph_generator::privacy_get_dual_edges(int dual_size)
    {
      return get_dual_edges(dual_g, dual_size);
    }

    int *dual_graph_generator::privacy_get_dual_edges()
    {
      return get_dual_edges(dual_g, dual_size);
    }

  private:
    dualgraph::graph dual_g;
  };
}
#endif //__CREATE_DUAL_GRAPH_HPP__