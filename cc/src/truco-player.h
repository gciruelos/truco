#include <array>
#include <vector>
#include <algorithm>

enum CardOrdering {
  EQ,
  LT,
  GT
};

enum EnvidoResponse {
  NO_QUIERO_E,
  ENVIDO0,
  ENVIDO1,
  REALENVIDO,
  FALTAENVIDO,
  QUIERO_E
};

enum TrucoLevel {
  NADA,
  TRUCO,
  RETRUCO,
  VALECUATRO
};

enum QuererResponse {
  NO_QUIERO,
  QUIERO
};

class Card;
class GameState;



class TrucoPlayer {
 public:
  size_t SayTanto();
  EnvidoResponse CantarEnvido(GameState state);
  EnvidoResponse AnswerEnvido(
      GameState state, std::vector<EnvidoResponse> responses);
  TrucoLevel CantarTruco(GameState state, TrucoLevel current_truco);
  QuererResponse AnswerTruco(GameState state, TrucoLevel new_truco);
};

class Card {
};

class Deck {
};

class GameState {
 public:
   size_t GetPoints(size_t player) const {
     return scores[player];
   }

   const std::vector<Card>& PlayedCards(size_t player) const {
     return played_cards[player];
   }

   const std::vector<size_t>& ManoInEachHand() const {
     return mano_in_each_hand;
   }

   bool AlguienTieneQuiero() const {
     return alguien_tiene_quiero;
   }

   size_t TieneQuiero() const {
     return tiene_quiero;
   }


 private:
  void AddPoints(size_t player, size_t points) {
    scores[player] += points;
  }

  void AddPlayedCard(size_t player, Card c) {
    played_cards[player].push_back(c);
    if (played_cards[player].size() > played_cards[1-player].size()) {
      mano_in_each_hand.push_back(player);
    }
  }


  void SetTieneQuiero(size_t jugador) {
    tiene_quiero = jugador;
    alguien_tiene_quiero = true;
  }

  void ClearAlguienTieneQuiero() {
    alguien_tiene_quiero = false;
  }

  std::array<size_t, 2> scores;
  std::array<std::vector<Card>, 2> played_cards;
  std::vector<size_t> mano_in_each_hand;
  bool alguien_tiene_quiero;
  bool tiene_quiero;


  friend class Game;
};


class Game {
 public:
  void DealCards();

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


  bool AskEnvido(size_t fst_player_index, bool fst_player_es_mano) {
    EnvidoResponse fst_player_envido =
        players[fst_player_index].CantarEnvido(state);
    std::vector<EnvidoResponse> responses = {fst_player_envido};
    bool cantado = fst_player_envido == ENVIDO0 ||
                   fst_player_envido == REALENVIDO ||
                   fst_player_envido == FALTAENVIDO;
    if (cantado) {
      size_t current_index = 1 - fst_player_envido;
      // Maximum 4 back-and-forth.
      for (size_t iterations = 0; iterations < 4; iterations++) {
        EnvidoResponse response =
          players[current_index].AnswerEnvido(state, responses);
        if (response <= responses.back()) {
          state.AddPoints(1 - current_index,
              EnvidoPoints(responses, false, state));
        } else if (response == QUIERO_E) {
          size_t winner = WinnerEnvido(fst_player_index, fst_player_es_mano);
          state.AddPoints(winner, EnvidoPoints(responses, true, state));
        } else {
          responses.push_back(response);
        }
      }
    }
    return cantado;
  }

  // Returns true iff hand ended.
  bool AskTruco(size_t player_index, TrucoLevel current_truco) {
    if ((state.AlguienTieneQuiero() && state.TieneQuiero() != player_index) ||
        current_truco == VALECUATRO) {
      return false;
    }

    TrucoLevel player_truco =
      players[player_index].CantarTruco(state, current_truco);

    if (player_truco == current_truco + 1) {
      QuererResponse response = players[1-player_index].AnswerTruco(
          state,
          player_truco);
      if (response == QUIERO) {
        state.SetTieneQuiero(1-player_index);
        return AskTruco(1-player_index, player_truco);
      } else {
        return true;
      }
    }
  }

  size_t WhoWonHand(size_t hand) {
    switch (state.PlayedCards(0)[hand].Compare(state.PlayedCards(1)[hand])) {
      case EQ:
        return state.ManoInEachHand()[hand];
      case LT:
        return 1;
      case GT:
        return 0;
    }
  }

  size_t WhoWonLastHand() {
    return WhoWonHand(
        std::min(state.PlayedCards(0).size(), state.PlayedCards(1).size()) - 1);
  }

  void PlayHand(size_t mano) {
    // First hand.
    bool mano_canto_envido = AskEnvido(mano, true);
    state.AddPlayedCard(mano, players[mano].PlayCard());
    if (!mano_canto_envido) {
      AskEnvido(1-mano, false);
    }
    state.AddPlayedCard(mano, players[1-mano].PlayCard());

    // Second hand.
    mano = WhoWonLastHand();
    AskTruco(mano, true);
    state.AddPlayedCard(mano, players[mano].PlayCard());
    AskTruco(1-mano, true);
    state.AddPlayedCard(1-mano, players[1-mano].PlayCard());

    // Third hand.
    mano = WhoWonLastHand();
    AskTruco(mano, true);
    state.AddPlayedCard(mano, players[mano].PlayCard());
    AskTruco(1-mano, true);
    state.AddPlayedCard(1-mano, players[1-mano].PlayCard());
  }

 private:
  std::array<TrucoPlayer, 2> players;
  GameState state;
};

