"""Your code. One stub per milestone; build them in order and keep each one small."""
import html
import math
import re
import unicodedata
import torch
import torch.nn as nn
from app.storage import Store

# Raw dataset of product descriptions with real-world noise (HTML tags, entities, boilerplate, extra whitespace).
RAW_CORPUS = [
    {
        "id": "hlg-001",
        "name": "Heritage Full-Grain Leather Briefcase",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p><strong>The Heritage Briefcase</strong> is handcrafted from the finest <em>full-grain vegetable-tanned leather</em>, 
            designed to age gracefully and develop a rich patina over time.</p>
            <div>Features include two spacious internal compartments, a padded 15-inch laptop sleeve, and solid brass hardware. &amp; 
            Reinforced double stitching ensures maximum durability for daily commuter use.</div>
            <p>SKU: HLG-001 | Price: $320.00 USD | In Stock</p>
            <p>Free shipping on orders over $50. 30-day hassle-free returns guarantee.</p>
        """
    },
    {
        "id": "hlg-002",
        "name": "Minimalist Bifold Wallet",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Sleek, pocket-friendly, and meticulously stitched by hand.&nbsp;Our <strong>Minimalist Bifold Wallet</strong> 
            features six dedicated card slots and a slim central billfold pocket for folded currency.</p>
            <span>Constructed from premium Italian bridle leather that softens and molds comfortably to your pocket.</span>
            <div>SKU: HLG-002 &bull; Price: $58.00</div>
            <p>Limited Edition - Buy now and save 15% today!</p>
        """
    },
    {
        "id": "hlg-003",
        "name": "Artisan Waxed Canvas & Leather Messenger",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <div>A timeless companion for photographers and urban explorers alike.</div>
            <p>This messenger combines water-resistant 18oz waxed canvas with thick oil-tanned leather accents and antiqued copper rivets.</p>
            <p>Equipped with an adjustable shoulder strap featuring an ergonomic padded leather sleeve, quick-release storm flap buckles, 
            and deep interior organizer pockets.&nbsp;&amp;&nbsp;Built to endure harsh weather while keeping your gear protected.</p>
            <p>SKU: HLG-003 | Free shipping on orders over $100.</p>
        """
    },
    {
        "id": "hlg-004",
        "name": "Classic Leather Duffle Weekender",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <h3>Engineered for the modern traveler.</h3>
            <p>The <strong>Classic Duffle Weekender</strong> offers generous packing volume encased in supple top-grain cowhide leather.</p>
            <p>Highlights include heavy-duty YKK two-way brass zippers, a dedicated shoe compartment with breathable grommets, 
            and reinforced wrap-around carry handles.&nbsp;Meets all standard airline carry-on size requirements.</p>
            <p>Price: $285.00 | SKU: HLG-004 | 30-day returns accepted.</p>
        """
    },
    {
        "id": "hlg-005",
        "name": "Vintage Leather Journal Cover",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Protect your thoughts and sketches in heirloom style.&nbsp;Our refillable <strong>Vintage Leather Journal Cover</strong> 
            is crafted from distressed pull-up leather that highlights natural grain variations and markings.</p>
            <div>Includes an integrated pen loop, ribbon bookmark, and an elastic wrap closure.&nbsp;Fits standard A5 notebooks 
            and moleskine inserts with ease. Hand-burnished beeswax edges offer a refined rustic aesthetic.</div>
            <p>SKU: HLG-005 &bull; In Stock</p>
        """
    },
    {
        "id": "hlg-006",
        "name": "Vegetable-Tanned Leather Belt",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Built from a single continuous strip of 10-12oz heavy vegetable-tanned steer hide leather.</p>
            <p>Featuring beveled, burnished edges treated with natural beeswax and secured with a removable solid brass buckle.</p>
            <div>Designed without synthetic fillers or glued layers, ensuring it will never split or crack under pressure.&nbsp;
            A reliable wardrobe cornerstone built for decades of daily wear.</div>
            <p>SKU: HLG-006 | Price: $75.00 USD</p>
        """
    },
    {
        "id": "hlg-007",
        "name": "Slim Front Pocket Cardholder",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Say goodbye to bulky back pockets.&nbsp;The <strong>Slim Front Pocket Cardholder</strong> holds up to eight cards 
            plus folded cash in a central compartment with zero extra bulk.</p>
            <div>Hand-cut from full-grain buttero leather and saddle-stitched with waxed linen thread for maximum tear resistance. 
            Smooth beveled edges ensure effortless gliding in and out of tight pockets.</div>
            <p>Price: $42.00 &bull; SKU: HLG-007</p>
        """
    },
    {
        "id": "hlg-008",
        "name": "Leather Field Watch Strap",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Upgrade your timepiece with rugged heritage elegance.&nbsp;Crafted from supple Horween Chromexcel leather, 
            this watch strap conforms comfortably to your wrist right out of the box.</p>
            <p>Finished with minimal hand-tied thread bar tacks and a brushed stainless steel buckle.&nbsp;
            Hypoallergenic lining repels sweat and daily moisture for long-lasting comfort.</p>
            <p>SKU: HLG-008 | Free shipping on orders over $50.</p>
        """
    },
    {
        "id": "hlg-009",
        "name": "Roll-Top Commuter Leather Backpack",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>A fusion of urban functionality and artisanal craft.&nbsp;The <strong>Roll-Top Commuter Backpack</strong> 
            features expandable cargo capacity secured by heavy leather utility straps and roller buckles.</p>
            <div>Padded shoulder straps distribute heavy loads evenly, while a quick-access side zipper allows direct access 
            to the internal 16-inch padded laptop sleeve without opening the main roll-top. Weather-resistant treated leather.</div>
            <p>SKU: HLG-009 | Price: $340.00 | In Stock</p>
        """
    },
    {
        "id": "hlg-010",
        "name": "Premium Padded Leather Laptop Sleeve",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Tailored specifically for sleek ultrabooks and laptops up to 14 inches.&nbsp;Constructed from rich oiled cowhide 
            lined with scratch-free micro-suede fleece padding.</p>
            <p>Features a secure magnetic flap closure that eliminates zipper scratches, paired with an exterior back slip pocket 
            for charging cables and slim notebooks. Clean, architectural lines for the modern professional.</p>
            <p>SKU: HLG-010 &bull; Price: $95.00</p>
        """
    },
    {
        "id": "hlg-011",
        "name": "Leather Travel Dopp Kit",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>A ruggedly sophisticated grooming organizer for long journeys and weekend escapes.</p>
            <div>The wide triangular opening stays propped open when unzipped, providing complete visibility of your toiletries. 
            Lined with water-resistant nylon canvas to handle accidental shampoo spills, encased in durable pull-up leather. 
            Includes a reinforced leather side grab handle for easy hanging.</div>
            <p>Price: $85.00 | SKU: HLG-011 | 30-day money-back guarantee.</p>
        """
    },
    {
        "id": "hlg-012",
        "name": "Hand-Stitched Leather Passport Wallet",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Travel effortlessly across continents with all your documents in one secure place.&nbsp;
            This passport wallet holds two passports, boarding passes, currency, and up to four cards.</p>
            <p>Hand-cut from full-grain English bridle leather, featuring hand-burnished edges and saddle-stitched borders. 
            Slim enough to fit comfortably inside a jacket breast pocket during security checks.</p>
            <p>SKU: HLG-012 | In Stock</p>
        """
    },
    {
        "id": "hlg-013",
        "name": "Executive Leather Desk Pad",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Elevate your workspace with a spacious, handcrafted desk pad made from smooth full-grain leather.</p>
            <div>Provides an ideal writing surface and smooth optical mouse tracking while protecting fine wood surfaces 
            from scratches, scuffs, and beverage rings. Backed with high-grip natural suede to prevent desktop slipping. 
            Dimensions: 32 inches by 16 inches.</div>
            <p>Price: $110.00 | SKU: HLG-013</p>
        """
    },
    {
        "id": "hlg-014",
        "name": "Rugged Leather Camera Strap",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Designed for DSLRs, mirrorless cameras, and vintage film rigs.&nbsp;Built from supple vegetable-tanned harness leather 
            that grows softer with every photo shoot.</p>
            <p>Includes protective leather bumper tabs around the steel split rings to prevent metal-on-camera friction scratches. 
            Tested to securely support camera bodies and heavy telephoto lenses up to 30 pounds.</p>
            <p>SKU: HLG-014 | Price: $65.00</p>
        """
    },
    {
        "id": "hlg-015",
        "name": "Compact Leather Coin Pouch",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>A palm-sized squeeze-frame leather pouch perfect for coins, guitar picks, and wireless earbuds.</p>
            <div>Constructed from supple pebbled calfskin with a flexible internal spring steel snap mechanism. 
            Squeeze the sides to open wide, release to snap shut securely. Eliminates rattling pocket change with artisanal elegance.</div>
            <p>SKU: HLG-015 &bull; Price: $28.00</p>
        """
    },
    {
        "id": "hlg-016",
        "name": "Braided Leather Key Clasp",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Keep your daily keys secure and within reach.&nbsp;Features an intricate four-strand round braid of hand-cut kangaroo lace, 
            anchored by a solid brass trigger snap hook and split ring.</p>
            <p>Attaches easily to belt loops or bag straps for rapid key access. Treated with conditioning oils for flexibility and weather resistance.</p>
            <p>SKU: HLG-016 | In Stock</p>
        """
    },
    {
        "id": "hlg-017",
        "name": "Artisan Leather Eyewear Case",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Protect your sunglasses and reading spectacles against crushing and scratches.</p>
            <div>Formed around a rigid internal nose bridge support that maintains shape under pressure. 
            Crafted from firm vegetable-tanned leather with a velvety microfiber lining and a brass stud collar closure. 
            Compact profile fits neatly into bags and vehicle compartments.</div>
            <p>Price: $55.00 | SKU: HLG-017</p>
        """
    },
    {
        "id": "hlg-018",
        "name": "Heritage Leather Tool & Pen Roll",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Organize your favorite writing instruments, carving tools, or art brushes in classic style.</p>
            <p>Features eight graduated pockets stitched into durable oil-waxed full-grain leather, protected by a fold-over protective flap. 
            Secures tightly with a wraparound leather thong and antique brass keeper ring.</p>
            <p>SKU: HLG-018 | Price: $78.00</p>
        """
    },
    {
        "id": "hlg-019",
        "name": "Zippered Leather Padfolio",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Make a lasting impression in client meetings and boardrooms.&nbsp;The <strong>Zippered Leather Padfolio</strong> 
            encloses a standard letter-size writing pad, tablet pocket, business card slots, and pen holder.</p>
            <div>Encased in rich mocha full-grain leather with an all-around smooth brass zipper to ensure loose documents stay put. 
            Hand-buffed edges and timeless minimalist silhouette.</div>
            <p>Price: $145.00 | SKU: HLG-019 | In Stock</p>
        """
    },
    {
        "id": "hlg-020",
        "name": "Handmade Leather Luggage Tag",
        "category": "Handcrafted Leather Goods",
        "raw_description": """
            <p>Spot your luggage instantly on the baggage carousel with distinctive artisanal flair.</p>
            <p>Crafted from thick vegetable-tanned saddle leather with a protective privacy flap that covers personal contact details. 
            Secures to your bag handle via a durable brass-buckled strap with reinforced eyelets.</p>
            <p>SKU: HLG-020 &bull; Price: $30.00 &bull; Buy now and save!</p>
        """
    }
]


def clean_text(text: str) -> str:
    """Clean raw product description text:
    - Decodes HTML entities (&amp;, &quot;, &#39;, &nbsp;, etc.)
    - Removes HTML tags and markup
    - Strips e-commerce boilerplate (SKU, price, shipping, return guarantees, stock alerts)
    - Normalizes unicode characters (quotes, dashes, non-breaking spaces)
    - Normalizes and collapses whitespace
    """
    if not text:
        return ""

    # Decode HTML entities
    cleaned = html.unescape(text)

    # Normalize unicode characters
    cleaned = unicodedata.normalize("NFKC", cleaned)
    cleaned = re.sub(r'[\u2018\u2019]', "'", cleaned)
    cleaned = re.sub(r'[\u201c\u201d]', '"', cleaned)
    cleaned = re.sub(r'[\u2013\u2014]', '-', cleaned)
    cleaned = cleaned.replace('\xa0', ' ')
    cleaned = cleaned.replace('&bull;', ' ')

    # Remove HTML tags
    cleaned = re.sub(r'<[^>]+>', ' ', cleaned)

    # Remove common boilerplate patterns
    boilerplate_patterns = [
        r'(?i)\bSKU\s*:\s*[A-Z0-9\-]+\b',
        r'(?i)\bPrice\s*:\s*\$[\d,]+(?:\.\d{2})?(?:\s*[A-Z]{3})?',
        r'(?i)\bFree shipping on orders over\s*\$[\d,]+[^\n\.\;]*[\.\n]?',
        r'(?i)\b\d+[- ]day (?:money[- ]back |hassle[- ]free )?(?:warranty|returns?|guarantee)[^\n\.\;]*[\.\n]?',
        r'(?i)\b(?:In Stock|Out of Stock|Limited Edition)\b',
        r'(?i)\bBuy now and save[^\n\.\;]*[\.\n]?',
    ]
    for pattern in boilerplate_patterns:
        cleaned = re.sub(pattern, ' ', cleaned)

    # Clean stray pipe/bullet separators left behind by removed boilerplate
    cleaned = re.sub(r'\s*[\|\u2022]\s*', ' ', cleaned)

    # Normalize whitespaces: collapse multiple spaces and newlines
    lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in cleaned.splitlines()]
    non_empty_lines = [line for line in lines if line]
    cleaned = ' '.join(non_empty_lines)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned


def collect_and_clean_corpus(category: str = "Handcrafted Leather Goods") -> list[dict]:
    """Collect raw product entries for the given category and clean their descriptions."""
    items = [item for item in RAW_CORPUS if item.get("category") == category]
    cleaned_items = []
    for item in items:
        cleaned_desc = clean_text(item["raw_description"])
        cleaned_items.append({
            "id": item["id"],
            "name": item["name"],
            "category": item["category"],
            "cleaned_description": cleaned_desc,
            "word_count": len(cleaned_desc.split()),
        })
    return cleaned_items


# --- Milestone 1: Collect a small corpus of product descriptions for a specific category.
# Hint: Focus on data collection and initial text cleaning.
def milestone_1(category: str = "Handcrafted Leather Goods", data_path: str | None = None) -> dict:
    """Executes Milestone 1:
    1. Collects raw product descriptions for a specific category.
    2. Cleans the text corpus (removes HTML, entities, boilerplate, and normalizes whitespace).
    3. Persists the cleaned corpus in Store.
    4. Returns summary metrics and data for downstream model training.
    """
    cleaned_corpus = collect_and_clean_corpus(category)
    total_words = sum(item["word_count"] for item in cleaned_corpus)

    store = Store(data_path)
    store.put("category", category)
    store.put("corpus", cleaned_corpus)
    store.put("total_products", len(cleaned_corpus))
    store.put("total_words", total_words)

    sample = cleaned_corpus[0] if cleaned_corpus else {}

    return {
        "category": category,
        "count": len(cleaned_corpus),
        "total_words": total_words,
        "corpus": cleaned_corpus,
        "sample": sample,
    }


# --- Milestone 2: Implement the byte-pair tokenizer and generate embeddings for product text.
# Hint: Implement byte-pair encoding and create an embedding layer.

class BPETokenizer:
    """Byte-Pair Encoding (BPE) Tokenizer built from scratch.
    - Base vocabulary: all 256 individual bytes (0-255) + special token <|endoftext|> (256)
    - Learns frequent byte-pair merges iteratively from training texts.
    - Guarantees lossless round-trip encoding and decoding for any UTF-8 string without UNK tokens.
    """
    SPECIAL_TOKENS = {
        "<|endoftext|>": 256,
    }

    def __init__(self, vocab_size: int = 350):
        self.target_vocab_size = vocab_size
        self.merges: dict[tuple[int, int], int] = {}
        self.vocab: dict[int, bytes] = {}
        self.special_tokens = dict(self.SPECIAL_TOKENS)
        self.inv_special_tokens = {v: k for k, v in self.special_tokens.items()}
        self._reset_base_vocab()

    def _reset_base_vocab(self):
        self.vocab = {i: bytes([i]) for i in range(256)}
        for name, token_id in self.special_tokens.items():
            self.vocab[token_id] = name.encode("utf-8")
        self.merges = {}

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

    @staticmethod
    def _get_stats(token_ids: list[int]) -> dict[tuple[int, int], int]:
        counts = {}
        for p in zip(token_ids, token_ids[1:]):
            counts[p] = counts.get(p, 0) + 1
        return counts

    @staticmethod
    def _merge_tokens(token_ids: list[int], pair: tuple[int, int], new_id: int) -> list[int]:
        new_ids = []
        i = 0
        p0, p1 = pair
        while i < len(token_ids):
            if i < len(token_ids) - 1 and token_ids[i] == p0 and token_ids[i + 1] == p1:
                new_ids.append(new_id)
                i += 2
            else:
                new_ids.append(token_ids[i])
                i += 1
        return new_ids

    def train(self, texts: list[str] | str, num_merges: int | None = None) -> None:
        """Trains BPE merges on input text(s) until target vocab_size or num_merges is reached."""
        self._reset_base_vocab()
        if isinstance(texts, list):
            text = "\n".join(texts)
        else:
            text = texts

        tokens = list(text.encode("utf-8"))
        if not tokens:
            return

        max_merges = num_merges if num_merges is not None else (self.target_vocab_size - len(self.vocab))

        for _ in range(max_merges):
            stats = self._get_stats(tokens)
            if not stats:
                break
            best_pair = max(stats.items(), key=lambda x: (x[1], -x[0][0], -x[0][1]))[0]
            if stats[best_pair] < 2:
                break

            new_id = len(self.vocab)
            tokens = self._merge_tokens(tokens, best_pair, new_id)
            self.merges[best_pair] = new_id
            self.vocab[new_id] = self.vocab[best_pair[0]] + self.vocab[best_pair[1]]

    def encode(self, text: str, allowed_special: bool = True) -> list[int]:
        """Encodes string into a list of token IDs using learned BPE merges."""
        if not text:
            return []

        if allowed_special and "<|endoftext|>" in text:
            parts = text.split("<|endoftext|>")
            encoded_tokens = []
            for idx, part in enumerate(parts):
                if part:
                    encoded_tokens.extend(self._encode_chunk(part))
                if idx < len(parts) - 1:
                    encoded_tokens.append(self.special_tokens["<|endoftext|>"])
            return encoded_tokens

        return self._encode_chunk(text)

    def _encode_chunk(self, text: str) -> list[int]:
        tokens = list(text.encode("utf-8"))
        if len(tokens) < 2:
            return tokens

        while len(tokens) >= 2:
            stats = self._get_stats(tokens)
            pair_to_merge = None
            min_rank = float("inf")
            for pair in stats:
                if pair in self.merges:
                    rank = self.merges[pair]
                    if rank < min_rank:
                        min_rank = rank
                        pair_to_merge = pair

            if pair_to_merge is None:
                break

            tokens = self._merge_tokens(tokens, pair_to_merge, self.merges[pair_to_merge])

        return tokens

    def decode(self, token_ids: list[int]) -> str:
        """Decodes a list of token IDs back into a UTF-8 string."""
        raw_bytes = bytearray()
        for token_id in token_ids:
            if token_id in self.vocab:
                raw_bytes.extend(self.vocab[token_id])
            elif token_id in self.inv_special_tokens:
                raw_bytes.extend(self.inv_special_tokens[token_id].encode("utf-8"))
            else:
                raw_bytes.extend(f"<unk:{token_id}>".encode("utf-8"))
        return raw_bytes.decode("utf-8", errors="replace")


class GPTEmbedding(nn.Module):
    """Embedding layer for GPT model combining token embeddings and positional embeddings."""
    def __init__(self, vocab_size: int, embed_dim: int = 64, max_seq_len: int = 256, dropout: float = 0.1):
        super().__init__()
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.max_seq_len = max_seq_len

        self.token_embedding = nn.Embedding(vocab_size, embed_dim)
        self.position_embedding = nn.Embedding(max_seq_len, embed_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        """
        input_ids: LongTensor of shape (batch_size, seq_len)
        Returns: Tensor of shape (batch_size, seq_len, embed_dim)
        """
        batch_size, seq_len = input_ids.shape
        if seq_len > self.max_seq_len:
            raise ValueError(f"Sequence length {seq_len} exceeds max_seq_len {self.max_seq_len}")

        positions = torch.arange(0, seq_len, dtype=torch.long, device=input_ids.device)
        tok_emb = self.token_embedding(input_ids)
        pos_emb = self.position_embedding(positions)
        return self.dropout(tok_emb + pos_emb)


def milestone_2(
    category: str = "Handcrafted Leather Goods",
    vocab_size: int = 350,
    embed_dim: int = 64,
    max_seq_len: int = 256,
    data_path: str | None = None,
) -> dict:
    """Executes Milestone 2:
    1. Loads the cleaned product corpus from Milestone 1 (or collects it if needed).
    2. Trains the Byte-Pair Encoding (BPE) tokenizer on the product descriptions.
    3. Builds the GPTEmbedding layer (Token + Positional embeddings).
    4. Encodes product descriptions and passes token IDs through the embedding layer.
    5. Saves tokenizer and embedding configurations to Store.
    6. Returns the trained tokenizer, embedding layer, and generated embedding tensors.
    """
    store = Store(data_path)
    corpus = store.get("corpus")
    if not corpus:
        m1_result = milestone_1(category=category, data_path=data_path)
        corpus = m1_result["corpus"]

    all_descriptions = [item["cleaned_description"] for item in corpus]

    # Train BPE tokenizer
    tokenizer = BPETokenizer(vocab_size=vocab_size)
    tokenizer.train(all_descriptions)

    # Initialize embedding layer
    embedding_layer = GPTEmbedding(
        vocab_size=tokenizer.vocab_size,
        embed_dim=embed_dim,
        max_seq_len=max_seq_len,
        dropout=0.0,
    )
    embedding_layer.eval()

    # Generate embeddings for a sample product description
    sample_item = corpus[0]
    sample_text = sample_item["cleaned_description"]
    sample_tokens = tokenizer.encode(sample_text)
    decoded_text = tokenizer.decode(sample_tokens)

    # Convert to PyTorch tensor of shape (1, seq_len)
    input_tensor = torch.tensor([sample_tokens], dtype=torch.long)
    with torch.no_grad():
        embeddings = embedding_layer(input_tensor)

    raw_bytes_len = len(sample_text.encode("utf-8"))
    num_tokens = len(sample_tokens)
    compression_ratio = round(raw_bytes_len / max(num_tokens, 1), 2)

    # Store metadata
    store.put("vocab_size", tokenizer.vocab_size)
    store.put("num_merges", len(tokenizer.merges))
    store.put("embed_dim", embed_dim)

    return {
        "tokenizer": tokenizer,
        "vocab_size": tokenizer.vocab_size,
        "num_merges": len(tokenizer.merges),
        "embedding_layer": embedding_layer,
        "sample_item": sample_item,
        "sample_text": sample_text,
        "sample_tokens": sample_tokens,
        "decoded_text": decoded_text,
        "compression_ratio": compression_ratio,
        "input_tensor_shape": list(input_tensor.shape),
        "embeddings_shape": list(embeddings.shape),
        "embeddings": embeddings,
    }


# --- Milestone 3: Build the causal self-attention mechanism and assemble the transformer block.
# Hint: Construct the causal self-attention mechanism and stack transformer blocks.

class CausalSelfAttention(nn.Module):
    """Multi-head Causal Self-Attention mechanism for autoregressive GPT.
    Ensures each position only attends to itself and previous positions.
    """
    def __init__(self, embed_dim: int = 64, num_heads: int = 4, max_seq_len: int = 256, dropout: float = 0.1):
        super().__init__()
        assert embed_dim % num_heads == 0, f"embed_dim ({embed_dim}) must be divisible by num_heads ({num_heads})"
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        self.max_seq_len = max_seq_len

        # Key, Query, Value projections in a single linear layer
        self.c_attn = nn.Linear(embed_dim, 3 * embed_dim)
        # Output projection
        self.c_proj = nn.Linear(embed_dim, embed_dim)

        self.attn_dropout = nn.Dropout(dropout)
        self.resid_dropout = nn.Dropout(dropout)

        # Causal mask: lower-triangular matrix of 1s
        # Tokens at index t can only attend to tokens at indices <= t
        self.register_buffer(
            "bias",
            torch.tril(torch.ones(max_seq_len, max_seq_len)).view(1, 1, max_seq_len, max_seq_len)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Tensor of shape (batch_size, seq_len, embed_dim)
        Returns:
            Tensor of shape (batch_size, seq_len, embed_dim)
        """
        B, T, C = x.shape
        if T > self.max_seq_len:
            raise ValueError(f"Sequence length {T} exceeds max_seq_len {self.max_seq_len}")

        # Compute queries, keys, and values
        qkv = self.c_attn(x)
        q, k, v = qkv.chunk(3, dim=-1)

        # Reshape to (B, num_heads, T, head_dim)
        q = q.view(B, T, self.num_heads, self.head_dim).transpose(1, 2)
        k = k.view(B, T, self.num_heads, self.head_dim).transpose(1, 2)
        v = v.view(B, T, self.num_heads, self.head_dim).transpose(1, 2)

        # Scaled dot-product attention: (B, nh, T, hs) x (B, nh, hs, T) -> (B, nh, T, T)
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(self.head_dim))
        # Mask out future positions (upper triangle)
        att = att.masked_fill(self.bias[:, :, :T, :T] == 0, float("-inf"))
        att = torch.softmax(att, dim=-1)
        att = self.attn_dropout(att)

        # Apply attention weights to values
        y = att @ v  # (B, num_heads, T, head_dim)
        # Re-assemble all head outputs
        y = y.transpose(1, 2).contiguous().view(B, T, C)

        return self.resid_dropout(self.c_proj(y))


class MLP(nn.Module):
    """Feed-forward network (MLP) within the Transformer block."""
    def __init__(self, embed_dim: int = 64, dropout: float = 0.1):
        super().__init__()
        self.c_fc = nn.Linear(embed_dim, 4 * embed_dim)
        self.act = nn.GELU()
        self.c_proj = nn.Linear(4 * embed_dim, embed_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.c_fc(x)
        x = self.act(x)
        x = self.c_proj(x)
        return self.dropout(x)


class TransformerBlock(nn.Module):
    """Pre-LayerNorm Transformer Block.
    x -> LayerNorm -> CausalSelfAttention + x -> LayerNorm -> MLP + x
    """
    def __init__(self, embed_dim: int = 64, num_heads: int = 4, max_seq_len: int = 256, dropout: float = 0.1):
        super().__init__()
        self.ln_1 = nn.LayerNorm(embed_dim)
        self.attn = CausalSelfAttention(embed_dim, num_heads, max_seq_len, dropout)
        self.ln_2 = nn.LayerNorm(embed_dim)
        self.mlp = MLP(embed_dim, dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x


class TransformerStack(nn.Module):
    """Stacks multiple TransformerBlocks with a final LayerNorm."""
    def __init__(self, num_layers: int = 2, embed_dim: int = 64, num_heads: int = 4, max_seq_len: int = 256, dropout: float = 0.1):
        super().__init__()
        self.num_layers = num_layers
        self.embed_dim = embed_dim
        self.layers = nn.ModuleList([
            TransformerBlock(embed_dim, num_heads, max_seq_len, dropout)
            for _ in range(num_layers)
        ])
        self.ln_f = nn.LayerNorm(embed_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for block in self.layers:
            x = block(x)
        return self.ln_f(x)


def verify_causality(attn_module: CausalSelfAttention, embed_dim: int = 64) -> bool:
    """Verifies that the attention module is strictly causal:
    Modifying future tokens at t' > t does not affect outputs at t.
    """
    attn_module.eval()
    with torch.no_grad():
        x1 = torch.randn(1, 4, embed_dim)
        x2 = x1.clone()
        x2[:, 3, :] = torch.randn(1, embed_dim)

        out1 = attn_module(x1)
        out2 = attn_module(x2)

        # Positions 0, 1, 2 must be mathematically identical
        return bool(torch.allclose(out1[:, :3, :], out2[:, :3, :], atol=1e-6))


def milestone_3(
    embed_dim: int = 64,
    num_heads: int = 4,
    num_layers: int = 2,
    max_seq_len: int = 256,
    data_path: str | None = None,
) -> dict:
    """Executes Milestone 3:
    1. Loads or executes Milestone 2 to obtain the embedding layer and sample product embeddings.
    2. Constructs the CausalSelfAttention mechanism with scaled dot-product and causal masking.
    3. Assembles the Pre-LayerNorm TransformerBlock with residual connections and MLP.
    4. Stacks multiple transformer blocks into a deep TransformerStack.
    5. Formally verifies the causality property (future tokens cannot influence past tokens).
    6. Passes sample embeddings through the transformer stack to generate output hidden states.
    7. Persists architectural parameters to Store and returns summary metrics.
    """
    m2_result = milestone_2(embed_dim=embed_dim, max_seq_len=max_seq_len, data_path=data_path)
    sample_embeddings = m2_result["embeddings"]  # Shape: (1, seq_len, embed_dim)

    # Instantiate attention, block, and stack
    attention = CausalSelfAttention(embed_dim=embed_dim, num_heads=num_heads, max_seq_len=max_seq_len, dropout=0.0)
    transformer_block = TransformerBlock(embed_dim=embed_dim, num_heads=num_heads, max_seq_len=max_seq_len, dropout=0.0)
    transformer_stack = TransformerStack(num_layers=num_layers, embed_dim=embed_dim, num_heads=num_heads, max_seq_len=max_seq_len, dropout=0.0)

    attention.eval()
    transformer_block.eval()
    transformer_stack.eval()

    # Verify causality
    causality_verified = verify_causality(attention, embed_dim=embed_dim)

    # Forward pass through block and full stack
    with torch.no_grad():
        block_output = transformer_block(sample_embeddings)
        stack_output = transformer_stack(sample_embeddings)

    total_block_params = sum(p.numel() for p in transformer_block.parameters())
    total_stack_params = sum(p.numel() for p in transformer_stack.parameters())

    store = Store(data_path)
    store.put("num_layers", num_layers)
    store.put("num_heads", num_heads)
    store.put("causality_verified", causality_verified)
    store.put("total_stack_params", total_stack_params)

    return {
        "causal_attention": attention,
        "transformer_block": transformer_block,
        "transformer_stack": transformer_stack,
        "embed_dim": embed_dim,
        "num_heads": num_heads,
        "num_layers": num_layers,
        "causality_verified": causality_verified,
        "total_block_params": total_block_params,
        "total_stack_params": total_stack_params,
        "input_embeddings_shape": list(sample_embeddings.shape),
        "block_output_shape": list(block_output.shape),
        "stack_output_shape": list(stack_output.shape),
        "stack_output": stack_output,
    }


# --- Milestone 4: Train the GPT model using the collected product descriptions.
# Hint: Set up the training loop with a loss function and optimizer.
def milestone_4():  # TODO(milestone 4)
    raise NotImplementedError("TODO(milestone 4)")


# --- Milestone 5: Implement a text generation feature that creates new product descriptions from a prompt.
# Hint: Implement text generation using sampling techniques.
def milestone_5():  # TODO(milestone 5)
    raise NotImplementedError("TODO(milestone 5)")


# --- Milestone 6: Develop a CLI for users to input product details and receive generated descriptions.
# Hint: Use a library like `argparse` to build the command-line interface.
def milestone_6():  # TODO(milestone 6)
    raise NotImplementedError("TODO(milestone 6)")
