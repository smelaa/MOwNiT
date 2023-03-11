#include <iostream>
#include <fstream>
#include <limits>

const int N=10000;

float next_x_v1(float xk){
    return xk+3*xk*(1-xk);
}
double next_x_v1(double xk){
    return xk+3*xk*(1-xk);
}

long double next_x_v1(long double xk){
    return xk+3*xk*(1-xk);
}

float next_x_v2(float xk){
    return 4*xk-3*xk*xk;
}

double next_x_v2(double xk){
    return 4*xk-3*xk*xk;
}

long double next_x_v2(long double xk){
    return 4*xk-3*xk*xk;
}

int main() {
    float float_v1[N]={0.1};
    double double_v1[N]={0.1};
    long double ldouble_v1[N]={0.1};
    float float_v2[N]={0.1};
    double double_v2[N]={0.1};
    long double ldouble_v2[N]={0.1};
    for (int i=1;i<N;i++){
        float_v1[i]= next_x_v1(float_v1[i-1]);
        double_v1[i]= next_x_v1(double_v1[i-1]);
        ldouble_v1[i]= next_x_v1(ldouble_v1[i-1]);
        float_v2[i]= next_x_v2(float_v2[i-1]);
        double_v2[i]= next_x_v2(double_v2[i-1]);
        ldouble_v2[i]= next_x_v2(ldouble_v2[i-1]);
    }
    std::ofstream file;
    file.open("wyniki.csv");
    file<<",x+3x(1-x) & float,x+3x(1-x) & double,x+3x(1-x) & long double,4x+3xx & float,4x+3xx & double,4x+3xx & long double,\n";
    file.precision(18);
    for (int i=0;i<N;i++){
        file<<i<<","<<float_v1[i]<<","<<double_v1[i]<<","<<ldouble_v1[i]<<","<<float_v2[i]<<","<<double_v2[i]<<","<<ldouble_v2[i]<<",\n";
    }
    file.close();
}
