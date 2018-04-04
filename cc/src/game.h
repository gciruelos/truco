

class Game {
 public:
  Game(TrucoPlayer* player0, TrucoPlayer* player1) {
    players[0] = player0;
    players[1] = player1;
  }

  void DealCards() {
    std::mt19937 g(rd());
    std::shuffle(deck.begin(), deck.end(), g);
    state.DealCards(0, deck[0], deck[2], deck[4]);
    state.DealCards(1, deck[1], deck[3], deck[5]);
  }

  void Play() {
    size_t mano = 0;
    while (true) {
      DealCards();
      PlayHand(mano);
      state.NewRound();
      mano = 1 - mano;
    }
  }

  size_t EnvidoPoints(
      std::vector<EnvidoResponse> envidos, bool querido,
      const GameState& state) {
    size_t score_player1 = state.GetPoints(0);
    size_t score_player2 = state.GetPoints(1);
    size_t min_score =
        (score_player1 < score_player2) ? score_player1 : score_player2;
    size_t max_score =
        (score_player2 < score_player1) ? score_player1 : score_player2;
    size_t falta_envido_querido =
        (max_score < 15) ?    // En las malas.
          (30 - min_score) :  // Maximo puntaje posible, gana el ganador.
          (30 - max_score);   // Lo que le falta al que va ganando.
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
      fst_player_tanto = players[fst_player_index]->SayTanto();
      snd_player_tanto = players[1-fst_player_index]->SayTanto();
    } else {
      snd_player_tanto = players[1-fst_player_index]->SayTanto();
      fst_player_tanto = players[fst_player_index]->SayTanto();
    }

    if (fst_player_tanto > snd_player_tanto) {
      return fst_player_index;
    } else if (fst_player_tanto < snd_player_tanto) {
      return 1 - fst_player_index;
    } else {
      return fst_player_es_mano ? fst_player_index : 1 - fst_player_index;
    }
  }


  bool AskEnvido(size_t cantador_index, bool cantador_es_mano) {
    EnvidoResponse cantador_envido =
        players[cantador_index]->CantarEnvido(state);
    std::vector<EnvidoResponse> responses = {cantador_envido};
    bool cantado = cantador_envido == ENVIDO0 ||
                   cantador_envido == REALENVIDO ||
                   cantador_envido == FALTAENVIDO;
    if (cantado) {
      size_t current_index = 1 - cantador_envido;
      // Maximum 4 back-and-forth.
      for (size_t iterations = 0; iterations < 4; iterations++) {
        EnvidoResponse response =
          players[current_index]->AnswerEnvido(state, responses);
        if (response <= responses.back()) {
          state.AddPoints(1 - current_index,
              EnvidoPoints(responses, false, state));
        } else if (response == QUIERO_E) {
          size_t winner = WinnerEnvido(cantador_index, cantador_es_mano);
          state.AddPoints(winner, EnvidoPoints(responses, true, state));
        } else {
          responses.push_back(response);
        }
      }
    }
    return cantado;
  }

  // Returns true iff hand ended.
  bool AskTruco(size_t player_index, size_t player_es_mano) {
    TrucoLevel current_truco = state.CurrentTruco();
    if ((state.AlguienTieneQuiero() && state.TieneQuiero() != player_index) ||
        current_truco == VALECUATRO) {
      return false;
    }

    TrucoLevel player_truco =
      players[player_index]->CantarTruco(state, current_truco);

    if (player_truco == current_truco + 1) {
      if (!state.EnvidoFueCantado() &&
          current_truco == NADA &&
          state.CurrentRonda() == 0) {
        AskEnvido(1-player_index, !player_es_mano);
      }
      QuererResponse response = players[1-player_index]->AnswerTruco(
          state,
          player_truco);
      if (response == QUIERO) {
        state.SetTieneQuiero(1-player_index);
        state.SetCurrentTruco(player_truco);
        return AskTruco(1-player_index, player_es_mano);
      } else {
        return true;
      }
    }
    return false;
  }

  size_t WhoWonHand(size_t hand) {
    switch (state.PlayedCards(0)[hand].Compare(state.PlayedCards(1)[hand])) {
      case EQ:
        return 2;  // Parda.
      case LT:
        return 1;
      case GT:
        return 0;
    }
  }

  size_t WhoWonLastHand() {
    return WhoWonHand(state.CurrentRonda() - 1);
  }

  void PlayHand(size_t mano) {
    size_t new_mano;
    // First hand.
    state.SetEnvidoFueCantado(AskEnvido(mano, true));
    AskTruco(mano, true);
    state.AddPlayedCard(mano, players[mano]->PlayCard(state));
    if (!state.EnvidoFueCantado()) {
      state.SetEnvidoFueCantado(AskEnvido(1-mano, false));
      AskTruco(1-mano, false);
    }
    state.AddPlayedCard(mano, players[1-mano]->PlayCard(state));

    // Second hand.
    new_mano = WhoWonLastHand();
    mano = new_mano == 2 ? mano : new_mano;
    AskTruco(mano, true);
    state.AddPlayedCard(mano, players[mano]->PlayCard(state));
    AskTruco(1-mano, false);
    state.AddPlayedCard(1-mano, players[1-mano]->PlayCard(state));

    // Third hand.
    new_mano = WhoWonLastHand();
    mano = new_mano == 2 ? mano : new_mano;
    AskTruco(mano, true);
    state.AddPlayedCard(mano, players[mano]->PlayCard(state));
    AskTruco(1-mano, false);
    state.AddPlayedCard(1-mano, players[1-mano]->PlayCard(state));
  }

 private:
  std::array<TrucoPlayer*, 2> players;
  GameState state;
  std::vector<Card> deck;

  std::random_device rd;
};
