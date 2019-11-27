int test (int a, int b, int c, int g) {
	int d, e;
	if (a)
		d = b * c;
	else
		d = b - c;
		e = b * c + g;
	return d + e;
}
