
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


