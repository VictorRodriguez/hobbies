int foo (int how) {
  switch (how) {
    case 2: how = 205; break;
    case 3: how = 305; break;
    case 4: how = 405; break;
    case 5: how = 505; break;
    case 6: how = 605; break;
  }
  return how;
}

void main(){
	int var = 3;
	foo(var);
}
