#include <array>
#include <vector>
#include <algorithm>
#include <set>
#include <random>

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

enum Palo {
  COPA,
  BASTO,
  ORO,
  ESPADA
};

class Card;
class GameState;



class TrucoPlayer {
 public:
  virtual size_t SayTanto() = 0;
  virtual EnvidoResponse CantarEnvido(const GameState& state) = 0;
  virtual EnvidoResponse AnswerEnvido(
      const GameState& state, const std::vector<EnvidoResponse>& responses) = 0;
  virtual TrucoLevel CantarTruco(
      const GameState& state, TrucoLevel current_truco) = 0;
  virtual QuererResponse AnswerTruco(
      const GameState& state, TrucoLevel new_truco) = 0;
  virtual Card PlayCard(const GameState& state) = 0;
};

class DumbTrucoPlayer : public TrucoPlayer {
 public:
  DumbTrucoPlayer(std::string name) : name_(name) {}
  size_t SayTanto();
  EnvidoResponse CantarEnvido(const GameState& state);
  EnvidoResponse AnswerEnvido(
      const GameState& state, const std::vector<EnvidoResponse>& responses);
  TrucoLevel CantarTruco(
      const GameState& state, TrucoLevel current_truco);
  QuererResponse AnswerTruco(
      const GameState& state, TrucoLevel new_truco);
  Card PlayCard(const GameState& state);
 private:
  std::string name_;
};

class HumanTrucoPlayer : public TrucoPlayer {
 public:
  size_t SayTanto();
  EnvidoResponse CantarEnvido(const GameState& state);
  EnvidoResponse AnswerEnvido(
      const GameState& state, const std::vector<EnvidoResponse>& responses);
  TrucoLevel CantarTruco(const GameState& state, TrucoLevel current_truco);
  QuererResponse AnswerTruco(const GameState& state, TrucoLevel new_truco);
  Card PlayCard(const GameState& state);
};



class Card {
 public:
  Card(size_t numero, Palo palo)
    : numero_(numero),
      palo_(palo) {
  }

  CardOrdering Compare(const Card& other_card) const {
    size_t rank_1 = CardRank();
    size_t rank_2 = other_card.CardRank();

    if (rank_1 < rank_2) {
      return LT;
    } else if (rank_1 > rank_2) {
      return GT;
    }
    return EQ;
  }

  bool operator==(const Card& other) const {
    return numero_ == other.numero_ && palo_ == other.palo_;
  }

  bool operator<(const Card& other) const {
    size_t rank_1 = CardRank();
    size_t rank_2 = other.CardRank();
    if (rank_1 == rank_2) {
      return palo_ < other.palo_;
    } else {
      return rank_1 < rank_2;
    }
  }


 private:
  size_t CardRank() const {
    switch (numero_) {
      case 4:
        return 0;
      case 5:
        return 1;
      case 6:
        return 2;
      case 7:
        if (palo_ == BASTO || palo_ == COPA) {
          return 3;
        } else if (palo_ == ORO) {
          return 10;
        }
        return 11;  // 7 de espadas.
      case 10:
        return 4;
      case 11:
        return 5;
      case 12:
        return 6;
      case 1:
        if (palo_ == BASTO || palo_ == ORO) {
          return 7;
        } else if (palo_ == BASTO) {
          return 12;
        }
        return 13;  // ancho de espadas.
      case 2:
        return 8;
      case 3:
        return 9;
      default:
        return 0;
    }
  }



  size_t numero_;
  Palo palo_;
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

   TrucoLevel CurrentTruco() const {
     return current_truco_;
   }

   size_t CurrentRonda() const {
     return std::min(PlayedCards(0).size(), PlayedCards(1).size());
   }

  bool EnvidoFueCantado() const {
    return envido_fue_cantado_;
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

  void DealCards(size_t player, Card c1, Card c2, Card c3) {
    holding_cards[player].clear();
    holding_cards[player].insert(c1);
    holding_cards[player].insert(c2);
    holding_cards[player].insert(c3);
  }

  void SetTieneQuiero(size_t jugador) {
    tiene_quiero = jugador;
    alguien_tiene_quiero = true;
  }

  void ClearAlguienTieneQuiero() {
    alguien_tiene_quiero = false;
  }

  void SetCurrentTruco(TrucoLevel new_level) {
    current_truco_ = new_level;
  }

  void SetEnvidoFueCantado(bool new_e) {
    envido_fue_cantado_ = new_e;
  }

  void NewRound() {
    played_cards[0].clear();
    played_cards[1].clear();
    mano_in_each_hand.clear();
    tiene_quiero = false;
    current_truco_ = NADA;
    envido_fue_cantado_ = false;
  }


  std::array<size_t, 2> scores;
  std::array<std::vector<Card>, 2> played_cards;
  std::array<std::set<Card>, 2> holding_cards;
  std::vector<size_t> mano_in_each_hand;
  bool alguien_tiene_quiero = false;
  size_t tiene_quiero;
  TrucoLevel current_truco_ = NADA;
  bool envido_fue_cantado_ = false;

  friend class Game;
};


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

