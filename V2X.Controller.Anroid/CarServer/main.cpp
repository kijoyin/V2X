#include <cstdio>

void log(char filename[], char visitor[])
{
	FILE * pLog;
	pLog = fopen(filename, "a");
	if (pLog != NULL)
	{
		fputs(visitor, pLog);
		fputs("\n", pLog);
		fclose(pLog);
	}
}

int main(int argc, char* argv[])
{
	if (argc != 2)
	{
		printf("Please pass filename as input parameter\n");
		return 1;
	}
	char input[20];
	printf("What IDE are you using?\n");
	scanf("%19[0-9a-zA-Z ]", input);
	printf("%s! You can use that with me?!\n", input);
	log(argv[1], input);
	return 0;
}