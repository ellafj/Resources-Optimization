#include <stdio.h>
#include <stdlib.h>

#define CHECK

#define MAX_LINE 255
#define BIGM    1000000

/**********************************************************************/
void write_solution(int nnodes, int z, int *x)
/**********************************************************************/
{
	FILE *fout = fopen("mysol.txt", "w");
#ifdef CHECK
	if ( fout == NULL ) 
	{
		printf("\nError: solution file mysol.txt cannot be written\n");
		exit(1);
	}
#endif
	fprintf(fout, "%d\n", z);
	int i;
	for ( i = 0; i < nnodes; i++ ) fprintf(fout, "%d\n", x[i]);
	fclose(fout);
	return;
}

/**********************************************************************/
void check_solution(int nnodes, int nedges, int *first, int *second, int *weight, int *x, int z)
/**********************************************************************/
{
	int zmax = 0;
	int i;
	for ( i = 0; i < nnodes; i++ ) 
	{
		if ( x[i] <= 0 ) 
		{
			printf("\nError: node %d has color %d\n", i+1, x[i]);
			exit(1);
		}
		if ( x[i] > zmax ) zmax = x[i];
	}
	if ( zmax != z ) 
	{
		printf("\nError: solution value %d vs %d\n", zmax, z);
		exit(1);
	}
	
	int e;
	for ( e = 0; e < nedges; e++ ) 
	{
		int f = first[e];
		int s = second[e];
		int distance = (x[f] > x[s]) ? (x[f] - x[s]) : (x[s] - x[f]);
		if ( distance < weight[e] )
		{
			printf("\nError: nodes %d and %d have distance %d vs %d (edge %d)\n", f+1, s+1, distance, weight[e], e+1);
			exit(1);
		}
	}
	
	printf("\nSolution is feasible and has value %d\n", z);
	return;
}


/**********************************************************************/
int greedy(int nnodes, int nedges, int *first, int *second, int *weight, int *x)
/**********************************************************************/
{
	int z = 0;
	int j;
	for ( j = 0; j < nnodes; j++ ) x[j] = -BIGM;
	for ( j = 0; j < nnodes; j++ )
	{
		int xmin = 1;
		int e;
		for ( e = 0; e < nedges; e++ )
		{
			int i = -1;
			if ( first[e] == j ) i = second[e];
			if ( second[e] == j ) i = first[e];
			if ( i >= 0 ) 
			{
				int color = x[i] + weight[e];
				if ( color > xmin ) xmin = color;
			}
		}
		x[j] = xmin;
		if ( xmin > z ) z = xmin;
	}
	
	return z;
}


/**********************************************************************/
int main(int argc, char** argv)
/**********************************************************************/
{
#ifdef CHECK
	if ( argc < 2 ) 
	{ 
		printf("Usage: %s -help for help\n", argv[0]); 
		exit(1); 
	}
#endif

/////////////////////////	
	// read the input file
/////////////////////////	
	FILE *fin = fopen(argv[1], "r");
#ifdef CHECK
	if ( fin == NULL ) 
	{
		printf("\nError: instance file %s cannot be read\n", argv[1]);
		exit(1);
	}
#endif
	int nnodes = 0;
	int nedges = 0;
	int counter = -1;
	int *first;
	int *second;
	int *weight;
	while ( counter < nedges )
	{
		char letter;
		char buffer[MAX_LINE];
		
		fscanf(fin, "%c", &letter);
		switch ( letter )
		{
			case 'p' :
			{
				char problem_type[10];
				fscanf(fin, "%s %d %d\n", problem_type, &nnodes, &nedges);
				nedges -= nnodes;
#ifdef CHECK
				if ( nnodes <= 0 ) 
				{
					printf("\nError: wrong number of nodes %d\n", nnodes);
					exit(1);
				}
				if ( nedges <= 0 ) 
				{
					printf("\nError: wrong number of edges %d\n", nedges);
					exit(1);
				}
#endif
				first = (int *) calloc(nedges, sizeof(int));
				second = (int *) calloc(nedges, sizeof(int));
				weight = (int *) calloc(nedges, sizeof(int));
				counter = 0;
				break;
			}
			case 'e' :
			{
				int f, s, w;
				fscanf(fin, "%d %d %d\n", &f, &s, &w);
				if ( f == s ) break;
#ifdef CHECK
				if ( counter >= nedges )
				{
					printf("\nError: wrong number of edges: only %d expected\n", nedges);
					exit(1);
					
				}
				if ( f<=0 || f>nnodes )
				{
					printf("\nError: wrong first node (%d) for edge %d\n", f, counter);
					exit(1);
				}
				if ( s<=0 || s>nnodes )
				{
					printf("\nError: wrong second node (%d) for edge %d\n", s, counter);
					exit(1);
				}
				if ( w<=0 || w>=BIGM )
				{
					printf("\nError: wrong weight (%d) for edge %d\n", w, counter);
					exit(1);
				}
#endif
				first[counter] = f - 1;
				second[counter] = s - 1;
				weight[counter] = w;
				counter++;
				break;
			}
			default :
			{
				fgets(buffer, MAX_LINE, fin);
				break;
			}
		}
	}
	fclose(fin);

	printf("\nThe graph has %d nodes and %d edges\n", nnodes, nedges);
	int e;
	for ( e = 0; e < nedges; e++ )
	{
		printf("edge %5d: nodes %5d and %5d, weight %5d\n", e+1, first[e]+1, second[e]+1, weight[e]);
	}


	if ( argc == 2 )
	{
		int i;
		// no input solution: apply a greedy
		int *x = (int *) calloc(nnodes, sizeof(int));
		int z = greedy(nnodes, nedges, first, second, weight, x);
#ifdef CHECK
		check_solution(nnodes, nedges, first, second, weight, x, z);
#endif
	
		write_solution(nnodes, z, x);
		printf("\nProblem %40s: solution value %4d\n",argv[1],  z);
		for ( i = 0; i < nnodes; i++ ) printf("node %5d -> color %5d\n", i+1, x[i]);
		free(x);
		
	}
	else 
	{
		// read the input solution
		fin = fopen(argv[2], "r");
#ifdef CHECK
		if ( fin == NULL ) 
		{
			printf("\nError: solution file %s cannot be read\n", argv[2]);
			exit(1);
		}
#endif
		int *x = (int *) calloc(nnodes, sizeof(int));
		int z = 0;
		fscanf(fin, "%d\n", &z);
		int i;
		for ( i = 0; i < nnodes; i++ ) fscanf(fin, "%d\n", &x[i]);
		fclose(fin);
		
#ifdef CHECK
		check_solution(nnodes, nedges, first, second, weight, x, z);
#endif
		
		printf("\nsolution value %d\n", z);
		for ( i = 0; i < nnodes; i++ ) printf("node %5d -> color %5d\n", i+1, x[i]);
		printf("CHK;%s;%d\n", argv[1], z);
		free(x);
	}

	exit(0);
}
