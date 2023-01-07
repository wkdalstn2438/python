// #include <stdio.h>
// qwer 한줄주석
/*   여러줄 주석
asdf
asdf
*/
/*
int main() {
	printf("Hello World\tqwer\n7656");
	return 0;
}
*/

// 두개의 숫자의 합을 계산하는 프로그램

// # include <stdio.h>
// main함수가 가장 먼저 시작하고 가장 늦게 끝남
/*
int main(void)
{
	// 선언 이후 참조
	int x;
	int y;
	int sum;

	x = 100;
	y = 200;
	sum = x + y;
	
	printf("두수의 합: %i", sum);

	return 0;
}
*/
/* #include <stdio.h>

int main(void)
{
	int x;
	int y;
	int sum;

	printf("첫번째 숫자를 입력하시오.");
	scanf("%d", &x);

	printf("두번째 숫자를 입력하시오.");
	scanf("%d", &y);

	sum = x + y;

	printf("두 수의 합: %d", sum);

	return 0;
}
*/
# include <stdio.h>

int main(void)
{
	double value;

	scanf("%lf", &value);
	printf("%lf", value);

	return 0;
}
