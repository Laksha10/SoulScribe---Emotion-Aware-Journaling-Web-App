import torch
import torch.nn as nn
from transformers import RobertaModel

class SoulScribeV8(nn.Module):
    def __init__(self):
        super(SoulScribeV8, self).__init__()
        self.roberta = RobertaModel.from_pretrained("roberta-large", output_hidden_states=True)
        self.gru = nn.GRU(
            input_size=1024,
            hidden_size=512,
            num_layers=1,
            bidirectional=True,
            batch_first=True,
        )
        self.attn = nn.Linear(1024, 1)
        self.dropout = nn.Dropout(0.3)
        self.projection = nn.Sequential(
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, 27)  # ✅ Only 27 labels in your trained model
        )
        self.temperature = nn.Parameter(torch.tensor(1.0))

    def forward(self, input_ids, attention_mask):
        output = self.roberta(input_ids=input_ids, attention_mask=attention_mask)
        hidden_states = torch.stack(output.hidden_states[-4:]).mean(0)
        x = hidden_states * attention_mask.unsqueeze(-1).float()
        gru_out, _ = self.gru(x)
        attn_scores = self.attn(gru_out).squeeze(-1)
        attn_weights = torch.softmax(attn_scores.masked_fill(attention_mask == 0, -1e9), dim=1)
        context = torch.sum(gru_out * attn_weights.unsqueeze(-1), dim=1)
        context = self.dropout(context)
        logits = self.projection(context) / self.temperature
        return torch.sigmoid(logits)
