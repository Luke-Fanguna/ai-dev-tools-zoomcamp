from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # enforce field validation at model save time so creating with empty
        # title ('' ) will raise ValidationError instead of silently writing
        # possibly-invalid rows to the DB.
        self.full_clean()
        super().save(*args, **kwargs)
