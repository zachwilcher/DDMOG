#include <cstdint>
#include <vector>
#include <iostream>
#include <Eigen/Core>
#include <stack>
#include <chrono>

int64_t count_ddmogs(const Eigen::VectorXi label_vec, const Eigen::MatrixXi A, const Eigen::Index vertex = 0) {
    int64_t nontrivial_count = 0;
    const Eigen::Index n = A.rows();

    if(vertex == n) {
        // check if the ddmog is trivial
        for(Eigen::Index i = 0; i < n; i++) {
            const int degree = A.row(i).sum() + A.col(i).sum();
            if(degree == 0) {
                return 0;
            }
        }
        return 1;
    }

    // compute weight of vertex
    const int weight = A.row(vertex).dot(label_vec) - label_vec.dot(A.col(vertex));

    //
    // Backtrack to solve sumset problem variant
    //

    const Eigen::Index l = n - vertex - 1;

    struct StackElement {
        const Eigen::VectorXi solution;
        const Eigen::Index index;
    };
    std::stack<StackElement> stack;

    stack.push({
        .solution = Eigen::VectorXi::Zero(l), 
        .index= l - 1
    });
    while(!stack.empty()) {
        const Eigen::VectorXi cur_solution = stack.top().solution;
        const Eigen::Index cur_index = stack.top().index;
        stack.pop();
        if(cur_index >= 0) {
            // backtrack for other solutions
            const Eigen::Index next_index = cur_index - 1;
            const Eigen::Index label_index = vertex + 1 + cur_index;

            stack.push({
                .solution = cur_solution, 
                .index = next_index
            });

            Eigen::VectorXi attempt2 = cur_solution;
            attempt2[cur_index] = -label_vec[label_index];
            stack.push({
                .solution = attempt2, 
                .index = next_index
            });

            Eigen::VectorXi attempt3 = cur_solution;
            attempt3[cur_index] = label_vec[label_index];
            stack.push({
                .solution = attempt3, 
                .index = next_index
            });

        } else if (cur_solution.sum() == -weight) {
            // Found a valid way to connect vertex to other vertices.
            // Construct new adjacency matrix and recurse.
            
            Eigen::MatrixXi new_A = A;


            for(Eigen::Index i = 0; i < l; i++) {
                Eigen::Index other_vertex = vertex + 1 + i;

                if(cur_solution[i] > 0) {
                    new_A(vertex, other_vertex) = 1;
                } else if (cur_solution[i] < 0) {
                    new_A(other_vertex, vertex) = 1;
                }
            }
            nontrivial_count += count_ddmogs(label_vec, new_A, vertex + 1);
        }
    }

    return nontrivial_count;
}

int main(int argc, char* argv[]) {
    if(argc != 2) {
        std::cout << "Usage: " << argv[0] << " <number of vertices>";
        return -1;
    }

    const Eigen::Index n = std::stoi(argv[1]);

    Eigen::VectorXi label_vec(n);
    for(Eigen::Index i = 0; i < n; i++) {
        int label = i + 1;
        label_vec[i] = label;
    }
    Eigen::MatrixXi A(n, n);
    A.fill(0);

    auto start = std::chrono::high_resolution_clock::now();
    int64_t nontrival_count = count_ddmogs(label_vec, A);
    auto stop = std::chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::seconds>(stop - start);

    std::cout << "Found " << nontrival_count << " DDMOGs with " << n << " vertices in " << duration.count() << " seconds.\n";
}