#define MAX 1000000

int a[256], b[256], c[256];

__attribute__((target_clones("avx2","arch=atom","default")))
void foo(){
int i,x;
for (x=0; x<MAX; x++){
    for (i=0; i<256; i++){
		a[i] = b[i] + c[i];
    }
}
}

int main() {
    foo();
    return 0;
}
