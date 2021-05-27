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


using namespace boost;
namespace planar_dual
{
  typedef adjacency_list<vecS,
                         vecS,
                         undirectedS,
                         property<vertex_index_t, int>,
                         property<edge_index_t, int>>
      graph;

  typedef property_map<graph, vertex_index_t>::type IndexMap_V;
  typedef property_map<graph, edge_index_t>::type IndexMap_E;
  typedef typename std::vector<int> vertex_vector_t;
  typedef iterator_property_map<typename vertex_vector_t::iterator, IndexMap_E>
      edge_to_face_map_t;

  // Hold data collection from visitor
  template <typename InputGraph,
            typename OutputVecA,
            typename OutputVecVecE,
            typename DualGraphVec>
  struct graph_face_vertex_visitor : public planar_face_traversal_visitor
  {
    graph_face_vertex_visitor(InputGraph &arg_g,
                              OutputVecA &arg_output_vector_v,
                              OutputVecVecE &arg_output_vector_e,
                              DualGraphVec &arg_output_graph_edge) : g(arg_g),
                                                                     output_vector_v(arg_output_vector_v),
                                                                     output_vector_e(arg_output_vector_e),
                                                                     output_vector_dual_e(arg_output_graph_edge),
                                                                     num_face(0),
                                                                     edge_to_face_vector(num_edges(g),
                                                                                         graph_traits<InputGraph>::null_vertex()),
                                                                     edge_to_face(edge_to_face_vector.begin(), index_e)

    {
    }
    void begin_face()
    {
      std::vector<vertex_vector_t>().swap(current_e);
      vertex_vector_t().swap(current_v);
      output_vector_v.push_back(vertex_vector_t());
      output_vector_e.push_back(std::vector<vertex_vector_t>());
    }
    void end_face()
    {
      std::vector<int>::iterator i;
      for (i = current_v.begin(); i < current_v.end(); i++)
      {
        output_vector_v[num_face].push_back(*i);
      }
      std::vector<std::vector<int>>::iterator j;
      for (j = current_e.begin(); j < current_e.end(); j++)
      {
        output_vector_e[num_face].push_back(*j);
      }
      num_face++;
    }

    template <typename Vertex>
    void next_vertex(Vertex v)
    {
      current_v.push_back(v);
    }

    template <typename Edge>
    void next_edge(Edge e)
    {
      // Belonging of edge in circle.
      vertex_vector_t e_vector(2);
      e_vector[0] = index_v[source(e, g)];
      e_vector[1] = index_v[target(e, g)];
      current_e.push_back(e_vector);

      // For Dual Graph (Circle connection).
      int existing_face = edge_to_face[e];
      if (existing_face == graph_traits<InputGraph>::null_vertex())
      {
        edge_to_face[e] = num_face;
      }
      else
      {
        vertex_vector_t e_vector(2);
        e_vector[0] = existing_face;
        e_vector[1] = num_face;
        output_vector_dual_e.push_back(e_vector);
      }
    }
    InputGraph &g;
    OutputVecA &output_vector_v;
    OutputVecVecE &output_vector_e;
    DualGraphVec &output_vector_dual_e;
    vertex_vector_t current_v;
    std::vector<vertex_vector_t> current_e;
    int num_face;
    IndexMap_V index_v = boost::get(vertex_index, g);
    IndexMap_E index_e = boost::get(edge_index, g);

    vertex_vector_t edge_to_face_vector;
    edge_to_face_map_t edge_to_face;
  };

  class graph_circle_finder
  {
  public:
    int edge_num;
    int *edge_origin;
    int planar_flag = 0;
    graph_circle_finder(const int edge_num, const int *edge_origin)
    {
      graph g;
      for (int i = 0; i < edge_num; i++)
      {
        add_edge(edge_origin[i * 2 + 0], edge_origin[i * 2 + 1], g);
      }
      property_map<planar_dual::graph, edge_index_t>::type e_index = get(edge_index, g);
      graph_traits<planar_dual::graph>::edges_size_type edge_count = 0;
      graph_traits<planar_dual::graph>::edge_iterator ei, ei_end;
      for (boost::tie(ei, ei_end) = edges(g); ei != ei_end; ++ei)
        put(e_index, *ei, edge_count++);
      //Check planarity.
      typedef std::vector<graph_traits<planar_dual::graph>::edge_descriptor> vec_t;
      std::vector<vec_t> embedding(num_vertices(g));
      if (boyer_myrvold_planarity_test(boyer_myrvold_params::graph = g,
                                       boyer_myrvold_params::embedding = &embedding[0]))
      {
        planar_flag = 1;
        graph_face_vertex_visitor<graph,
                                  std::vector<std::vector<int>>,
                                  std::vector<std::vector<std::vector<int>>>,
                                  std::vector<std::vector<int>>>
            face_vis(g,
                     vector_v,
                     vector_e,
                     vector_dual_edge);
        planar_face_traversal(g, &embedding[0], face_vis);
      }
      else
      {
        planar_flag = -1;
        exit(-1);
      }
    }

    int privacy_get_graph_face_num()
    {
      return vector_e.size();
    }
    int privacy_get_graph_dual_edges_num()
    {
      return vector_dual_edge.size();
    }
    int privacy_get_face_vertex_num_sum()
    {
      int idx = 0;
      for (int i = 0; i < vector_v.size(); i++)
        idx += vector_v[i].size();
      return idx;
    }
    void get_circle_vertex_num_list(std::vector<int> *vertex_num_list)
    {

      for (int i = 0; i < vector_v.size(); i++)
        (*vertex_num_list)[i] = vector_v[i].size();
    }
    void get_circle_edge_num_list(std::vector<int> *edge_num_list)
    {
      get_circle_vertex_num_list(edge_num_list);
    }
    void get_circle_vertex_list(std::vector<int> *vertex_num_list, std::vector<int> *vertex_list)
    {
      int idx_vertex = 0;
      for (int i = 0; i < vector_v.size(); i++)
      {
        for (int j = 0; j < (*vertex_num_list)[i]; j++)
        {
          (*vertex_list)[idx_vertex + j] = vector_v[i][j];
        }
        idx_vertex += (*vertex_num_list)[i];
      }
    }
    void get_circle_edge_list(std::vector<int> *edge_num_list, std::vector<std::vector<int>> *edge_list)
    {
      int idx_edge = 0;
      for (int i = 0; i < vector_e.size(); i++)
      {
        for (int j = 0; j < (*edge_num_list)[i]; j++)
        {
          (*edge_list)[idx_edge + j] = vector_e[i][j];
        }
        idx_edge += (*edge_num_list)[i];
      }
    }

    int privacy_get_dual_edge_num()
    {
      return vector_dual_edge.size();
    }

    void get_dual_edge_list(int dual_edge_num, std::vector<std::vector<int>> *edge_list)
    {
      for (int i = 0; i < dual_edge_num; i++)
      {
        (*edge_list)[i][0] = vector_dual_edge[i][0];
        (*edge_list)[i][1] = vector_dual_edge[i][1];
      }
    }

    std::vector<std::vector<int>> get_vector_v()
    {
      return vector_v;
    }

    std::vector<std::vector<std::vector<int>>> get_vector_e()
    {
      return vector_e;
    }

    std::vector<std::vector<int>> get_vector_dual_edge()
    {
      return vector_dual_edge;
    }

  private:
    graph g;
    std::vector<std::vector<int>> vector_v;
    std::vector<std::vector<std::vector<int>>> vector_e;
    std::vector<std::vector<int>> vector_dual_edge;
  };
}
#endif //__CREATE_DUAL_GRAPH_HPP__