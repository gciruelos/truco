#include "truco-player.h"



size_t DumbTrucoPlayer::SayTanto() {
  return 20;
}

EnvidoResponse DumbTrucoPlayer::CantarEnvido(const GameState& state) {
  return NO_QUIERO_E;
}

EnvidoResponse DumbTrucoPlayer::AnswerEnvido(
    const GameState& state,
    const std::vector<EnvidoResponse>& responses) {
  return NO_QUIERO_E;
}

TrucoLevel DumbTrucoPlayer::CantarTruco(
    const GameState& state, TrucoLevel current_truco) {
  return NADA;
}

QuererResponse DumbTrucoPlayer::AnswerTruco(
    const GameState& state, TrucoLevel new_truco) {
  return NO_QUIERO;
}


