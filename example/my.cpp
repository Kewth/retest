#include <cstdio>

int main() {
	freopen("my.in", "r", stdin);
	freopen("my.out", "w", stdout);
	int n;
	scanf("%d", &n);
	if(n <= 3) puts("ANS");
	else if(n <= 5) while(true);
	else if(n <= 7) return -1;
	else if(n <= 10) puts("...");
}
