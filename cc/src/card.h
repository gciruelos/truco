


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
