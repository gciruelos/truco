#include "truco-player.h"



size_t TrucoPlayer::SayTanto() {
  return 20;
}

EnvidoResponse TrucoPlayer::CantarEnvido(GameState state) {
  return NO_QUIERO_E;
}

EnvidoResponse TrucoPlayer::AnswerEnvido(
    GameState state, std::vector<EnvidoResponse> responses) {
  return NO_QUIERO_E;
}

TrucoLevel TrucoPlayer::CantarTruco(GameState state, TrucoLevel current_truco) {
  return NADA;
}

QuererResponse TrucoPlayer::AnswerTruco(
    GameState state, TrucoLevel new_truco) {
  return NO_QUIERO;
}


