#include <cstdint>
#include <Eigen/Core>
#include <chrono>
#include <iostream>

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

    Eigen::VectorXi solution = (A - A.transpose()).row(vertex);

    bool done = false;
    while(!done) {

        if(solution.dot(label_vec) == 0) {
            Eigen::MatrixXi new_A = A;
            for(Eigen::Index other_vertex = vertex + 1; other_vertex < n; other_vertex++) {
                if(solution[other_vertex] > 0) {
                    new_A(vertex, other_vertex) = 1;
                } else if (solution[other_vertex] < 0) {
                    new_A(other_vertex, vertex) = 1;
                }
            }
            nontrivial_count += count_ddmogs(label_vec, new_A, vertex + 1);
        }

        // increment
        bool carry = true;
        Eigen::Index index = vertex + 1;
        while(carry && (index < n)) {
            switch(solution[index]) {
                case 0:
                    solution[index] = -1;
                    carry = false;
                    break;
                case -1:
                    solution[index] = 1;
                    carry = false;
                    break;
                case 1:
                    solution[index] = 0;
                    break;
            }
            // This is slower than the switch statement above.
            // solution[index] = ((solution[index] + 3) % 3) - 1;
            // carry = solution[index] == 0;
            index++;
        }
        if(carry) {
            done = true;
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

    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(stop - start);

    std::cout << "Found " << nontrival_count << " DDMOGs with " << n << " vertices in " << duration.count() << "ms\n";
}