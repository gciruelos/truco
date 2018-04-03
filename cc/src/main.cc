#include <iostream>

#include "truco-player.h"

int main() {
  DumbTrucoPlayer p1("jorge"), p2("carlos");
  Game g(&p1, &p2);
  g.Play();


  return 0;
}
