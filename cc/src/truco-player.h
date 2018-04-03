
class TrucoPlayer {
};

class Deck {
};

class GameState {
 public:


 private:
  size_t score_player1;
  size_t score_player2;
  size_t round_number;
  size_t size;
};


enum EnvidoResponse {
  NO_QUIERO,
  ENVIDO0,
  ENVIDO1,
  REALENVIDO,
  FALTAENVIDO,
  QUIERO
};

enum EnvidoType {
  ENVIDO,
  REALENVIDO,
  FALTAENVIDO,
  ENVIDO_ENVIDO,
  ENVIDO_REALENVIDO,
  ENVIDO_FALTAENVIDO,
  REALENVIDO_FALTAENVIDO,
  ENVIDO_ENVIDO_REALENVIDO,
  ENVIDO_ENVIDO_FALTAENVIDO,
  ENVIDO_REALENVIDO_FALTAENVIDO,
  ENVIDO_ENVIDO_REALENVIDO_FALTAENVIDO,
};

class Game {
 public:
  void DealCards();

  size_t EnvidoPoints(
      std::vector<EnvidoResponse> envidos, bool querido,
      size_t score_player1, size_t score_player2) {
    size_t min_score =
        (score_player1 < score_player2) ? score_player1 : score_player2;
    size_t max_score =
        (score_player2 < score_player1) ? score_player1 : score_player2;
    size_t falta_envido_querido =
        max_score < 15 ?     // En las malas.
          (30 - min_score)   // Maximo puntaje posible, gana el ganador.
          (30 - max_score);  // Lo que le falta al que va ganando.
    size_t valor_querido = 0;
    size_t valor_noquerido = 0;
    for (const auto envido : envidos) {
      switch (envido) {
        case ENVIDO0:
        case ENVIDO1:
          valor_querido += 2;
          valor_noquerido++;
          break;
        case REALENVIDO:
          valor_querido += 3;
          valor_noquerido++;
          break;
        case FALTAENVIDO:
          valor_querido = falta_envido_querido;
          valor_noquerido++;
          break;
        default:
          break;
      }
    }
    return querido ? valor_querido : valor_noquerido;
  }

  size_t WinnerEnvido(size_t fst_player_index, bool fst_player_es_mano) {
    size_t fst_player_tanto, snd_player_tanto;
    if (fst_player_es_mano) {
      fst_player_tanto = players[fst_player_index].SayTanto();
      snd_player_tanto = players[1-fst_player_index].SayTanto();
    } else {
      snd_player_tanto = players[1-fst_player_index].SayTanto();
      fst_player_tanto = players[fst_player_index].SayTanto();
    }

    if (fst_player_tanto > snd_player_tanto) {
      return fst_player_index;
    } else if (fst_player_tanto < snd_player_tanto) {
      return 1 - fst_player_index;
    } else {
      return fst_player_es_mano ? fst_player_index : 1 - fst_player_index;
    }
  }


  void AskEnvido(size_t fst_player_index, bool fst_player_es_mano) {
    EnvidoResponse fst_player_envido =
        players[fst_player_index].CantarEnvido(state);
    bool cantado = false;
    std::vector<EnvidoResponse> responses = {fst_player_envido};
    switch (fst_player_envido) {
      case ENVIDO0:
      case REALENVIDO:
      case FALTAENVIDO:
        cantado = true;
        size_t current_index = 1 - fst_player_envido;
        for (size_t iterations = 0; iterations < 4; iterations++) {   // Maximum 4 back-and-forth.
          EnvidoResponse response = players[current_index].AnswerEnvido(state, responses);
          if (response <= responses.back()) {
            state.AddPoints(1 - current_index, EnvidoPoints(responses, false, state.GetPoints(0), states.GetPoints(1)));
          } else if (response == QUIERO) {
            size_t winner = WinnerEnvido(fst_player_index, fst_player_es_mano);
            state.AddPoints(winner, EnvidoPoints(responses, true, state.GetPoints(0), states.GetPoints(1)));
          } else {
            responses.push_back(fst_player_response);
          }
        }
        break;
      default:
        break;
    }
    return cantado;
  }

  void PlayHand(size_t mano) {
    TrucoPlayer& fst_player = players[mano];
    TrucoPlayer& snd_player = players[1-mano];


  }
 private:
  std::array<Truco
};

